from aiogram import Dispatcher, Bot

from bot.handlers.admin import register_admin_handlers
from bot.handlers.other import register_other_handlers
from bot.handlers.user import register_user_handlers


def register_all_handlers(dp: Dispatcher, bot: Bot) -> None:
    handlers = (
        register_admin_handlers,
        register_other_handlers,
    )

    register_user_handlers(dp, bot)
    for handler in handlers:
        handler(dp)
