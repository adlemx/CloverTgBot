from aiogram import Dispatcher, types, Bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ContentType

# ReplyKeyboardMarkup(resize_keyboard=True).add(
#             KeyboardButton('Отправить свой контакт ☎️', request_contact=True)
#         ).add(
#             KeyboardButton('Отправить свою локацию 🗺️', request_location=True)
#         )
from bot.database.methods.get import get_product
from bot.misc import env, TgKeys

message_id = 0


def register_user_handlers(dp: Dispatcher):
    @dp.message_handler(commands=['start', 'help'])
    async def send_welcome(message: types.Message):
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
        print(message.location)
        message_id = message.message_id
        await message.answer(f'Ваша позиция: {message.location}')

    @dp.callback_query_handler(lambda c: c.data and c.data.startswith('product'))
    async def process_callback_preorder(callback_query: types.CallbackQuery):
        code = callback_query.data.replace('product', '')
        if code.isdigit(): code = int(code)
        product = get_product(code)
        if product is None: return None
        markup_request = InlineKeyboardMarkup(row_width=1) \
            .add(InlineKeyboardButton('Оплатить', callback_data=f'order{code}'))
        await dp.bot.edit_message_text(f"Ваш заказ:\n"
                                       f"Товар: {product.name}\n"
                                       f"Описание товара: {product.description}\n"
                                       f"Стоимость: {product.price / 100}",
                                       message_id=callback_query.message.message_id,
                                       chat_id=callback_query.message.chat.id,
                                       reply_markup=markup_request)

    @dp.callback_query_handler(lambda c: c.data and c.data.startswith('order'))
    async def process_callback_preorder(callback_query: types.CallbackQuery):
        code = callback_query.data.replace('order', '')
        if code.isdigit(): code = int(code)
        product = get_product(code)
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
            payload=f'pay{code}'
        )

    @dp.pre_checkout_query_handler(lambda query: True)
    async def pre_check_out(pre_checkout_query: types.PreCheckoutQuery):
        print("payed")
        await dp.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

    @dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
    async def process_successful_payment(message: types.Message):
        product_id = message.successful_payment.invoice_payload.replace('pay', '')
        print(message.successful_payment)
        print(message.location)
        product = get_product(int(product_id))
        await message.answer("Спасибо за покупку мы уже собираем ваш заказ\n"
                             f"В посылке: {product.name}")