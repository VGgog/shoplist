from aiogram import Dispatcher

from handlers import handler


def register_handlers(dp: Dispatcher):
    """
    Register all handlers.
    """
    dp.register_message_handler(handler.start_menu, commands="start")


def register_buttons_callback(dp: Dispatcher):
    """
    Register callback for buttons.
    """
    dp.register_callback_query_handler(handler.callback_buttons_handler, lambda callback_query: True)

