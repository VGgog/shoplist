from aiogram import Dispatcher

from handlers import handler


def register_handlers(dp: Dispatcher):
    """Register all handlers"""
    dp.register_message_handler(handler.start_menu, commands="start")

