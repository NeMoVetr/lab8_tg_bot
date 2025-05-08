from aiogram import Dispatcher

from bot.handlers import messages
from bot.keyboards import inline


def setup_routers(dp: Dispatcher):
    dp.include_routers(
        messages.router,
        inline.router,
    )


__all__ = "setup_routers"