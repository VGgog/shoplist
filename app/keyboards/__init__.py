from aiogram import Dispatcher
from keyboards import callbacks


def register_buttons_callback(dp: Dispatcher):
    """
    Register callback for buttons.
    """
    dp.register_callback_query_handler(callbacks.callback_buttons_handler, lambda callback_query: True)
