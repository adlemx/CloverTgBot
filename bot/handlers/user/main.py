from aiogram import Dispatcher, types, Bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


# ReplyKeyboardMarkup(resize_keyboard=True).add(
#             KeyboardButton('Отправить свой контакт ☎️', request_contact=True)
#         ).add(
#             KeyboardButton('Отправить свою локацию 🗺️', request_location=True)
#         )



def register_user_handlers(dp: Dispatcher, bot: Bot):
    # todo: register all user handlers
    @dp.message_handler(commands=['start', 'help'])
    async def send_welcome(message: types.Message):
        await message.answer("С помощью этого бота вы сможете заказать доставку дроном \n"
                             "для заказа напишите /order")

    @dp.message_handler(commands=['order'])
    async def start_order(message: types.Message):
        markup_request = InlineKeyboardMarkup(row_width=1)\
            .add(InlineKeyboardButton('1', callback_data='product1'))\
            .add(InlineKeyboardButton('2', callback_data='product2'))\
            .add(InlineKeyboardButton('3', callback_data='product3'))
        await message.answer("Выберите товар который вы хотите заказать", reply_markup=markup_request)

    @dp.callback_query_handler(lambda c: c.data and c.data.startswith('product'))
    async def process_callback_preorder(callback_query: types.CallbackQuery):
        code = callback_query.data[-1]
        if code.isdigit(): code = int(code)
        markup_request = InlineKeyboardMarkup(row_width=1)\
            .add(InlineKeyboardButton('Оплатить', callback_data=f'order{code}'))
        await bot.edit_message_text(f"Ваш заказ:\n"
                                    f"Товар: {code}\n"
                                    f"Стоимость: {code*10}", message_id=callback_query.message.message_id, chat_id=callback_query.message.chat.id,
                                    reply_markup=markup_request)

    @dp.callback_query_handler(lambda c: c.data and c.data.startswith('order'))
    async def process_callback_preorder(callback_query: types.CallbackQuery):
        code = callback_query.data[-1]
        if code.isdigit(): code = int(code)

