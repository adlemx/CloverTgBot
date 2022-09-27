import base64
import io

import qrcode
from aiogram import Dispatcher, types, Bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ContentType

# ReplyKeyboardMarkup(resize_keyboard=True).add(
#             KeyboardButton('Отправить свой контакт ☎️', request_contact=True)
#         ).add(
#             KeyboardButton('Отправить свою локацию 🗺️', request_location=True)
#         )
from bot.database.methods.create import create_order, create_user
from bot.database.methods.get import get_product, get_user, get_order
from bot.database.methods.update import change_order_state, set_address, set_phone, new_order
from bot.database.models.main import OrderStates
from bot.misc import env, TgKeys
from bot.misc.util import generate_qr

message_id = 0
disp: Dispatcher


def register_user_handlers(dp: Dispatcher):
    disp = dp

    @dp.message_handler(commands=['start', 'help'])
    async def send_welcome(message: types.Message):
        user = get_user(message.from_user.id)
        if user is None: user = create_user(message.from_user.id)
        print(user.orders)
        await message.answer("С помощью этого бота вы сможете заказать доставку дроном \n"
                             "для заказа напишите /order")

    @dp.message_handler(commands=['order'])
    async def start_order(message: types.Message):
        markup_request = InlineKeyboardMarkup(row_width=1) \
            .add(InlineKeyboardButton('1', callback_data='product1')) \
            .add(InlineKeyboardButton('2', callback_data='product2')) \
            .add(InlineKeyboardButton('3', callback_data='product3'))
        await message.answer("Выберите товар который вы хотите заказать", reply_markup=markup_request)

    @dp.message_handler(content_types=[ContentType.LOCATION])
    async def set_pos(message: types.Message):
        data = await dp.storage.get_data(chat=message.chat.id, user=message.from_user.id)
        print(data)
        if data.get("type") == "get_loc":
            order_id = data.get("order_id")
            await message.delete()
            markup_request = InlineKeyboardMarkup(row_width=1) \
                .add(InlineKeyboardButton('Оплатить', callback_data=f'order{order_id}'))
            set_address(order_id, str(message.location))
            await dp.storage.set_data(chat=message.chat.id, user=message.from_user.id,
                                      data={})
            await dp.bot.edit_message_text("Отлично, теперь осталось только оплатить заказ",
                                           message_id=data.get("msg_id"), reply_markup=markup_request,
                                           chat_id=message.chat.id)

    @dp.callback_query_handler(lambda c: c.data and c.data.startswith('product'))
    async def process_callback_preorder(callback_query: types.CallbackQuery):
        code = callback_query.data.replace('product', '')
        if code.isdigit(): code = int(code)
        product = get_product(code)
        if product is None: return None
        markup_request = InlineKeyboardMarkup(row_width=1) \
            .add(InlineKeyboardButton('Отправить геопозицию', callback_data=f'location{code}'))
        await dp.bot.edit_message_text(f"Ваш заказ:\n"
                                       f"Товар: {product.name}\n"
                                       f"Описание товара: {product.description}\n"
                                       f"Стоимость: {product.price / 100}",
                                       message_id=callback_query.message.message_id,
                                       chat_id=callback_query.message.chat.id,
                                       reply_markup=markup_request)

    @dp.callback_query_handler(lambda c: c.data and c.data.startswith('location'))
    async def process_callback_get_location(callback_query: types.CallbackQuery):
        code = callback_query.data.replace('location', '')
        if code.isdigit(): code = int(code)
        order = create_order(callback_query.from_user.id, "", "", "", code)
        await dp.storage.set_data(chat=callback_query.message.chat.id, user=callback_query.from_user.id,
                                  data={'type': "get_loc", 'order_id': order.order_id,
                                        'msg_id': callback_query.message.message_id})
        await callback_query.message.edit_text("Жду адрес доставки")

    @dp.callback_query_handler(lambda c: c.data and c.data.startswith('order'))
    async def process_callback_preorder(callback_query: types.CallbackQuery):
        code = callback_query.data.replace('order', '')
        if code.isdigit(): code = int(code)
        order = get_order(code)
        product = get_product(order.product)
        if product is None: return None
        PRICE = types.LabeledPrice(label=product.name, amount=product.price)
        await dp.bot.send_invoice(
            callback_query.message.chat.id,
            title=product.name,
            description=product.description,
            provider_token=TgKeys.PAYTOKEN,
            currency='rub',
            need_phone_number=True,
            # need_shipping_address=True,
            is_flexible=False,  # True если конечная цена зависит от способа доставки
            prices=[PRICE],
            start_parameter=f'{code}',
            payload=f'id{order.order_id}'
        )

    @dp.pre_checkout_query_handler(lambda query: True)
    async def pre_check_out(pre_checkout_query: types.PreCheckoutQuery):
        product_id = pre_checkout_query.invoice_payload.replace('id', '')
        change_order_state(int(product_id), OrderStates.PAYMENT_REQUIRED)
        print("payed")
        await dp.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

    @dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
    async def process_successful_payment(message: types.Message):
        order_id = message.successful_payment.invoice_payload.replace('id', '')
        change_order_state(int(order_id), OrderStates.ASSEMBLING)
        set_phone(int(order_id), message.successful_payment.order_info.phone_number)
        print(message.successful_payment)
        print(message.location)
        order = get_order(int(order_id))
        if order is None: return None
        base = generate_qr(order.code)
        base.seek(0)
        await message.answer_photo(
            photo=('qr.png', base),
            caption="Получить посылку вы сможете по этому qr коду"
        )
        await message.answer("Спасибо за покупку мы уже собираем ваш заказ")


def delivery_started(order_id: int):
    order = get_order(order_id)
    if order is None: return None
    change_order_state(order_id, OrderStates.DELIVERY)
    disp.bot.send_message(order.tg_id, "Ваш заказ уже отправлен")


def check_code(order_id: int, code: int):
    order = get_order(order_id)
    if order is None: return None
    if order.code == code:
        change_order_state(order_id, OrderStates.DONE)
        disp.bot.send_message(order.tg_id, "Заказ получен")
        new_order(order.tg_id)
    else:
        disp.bot.send_message(order.tg_id, "Вы использовали не тот qr code для получения посылки")

