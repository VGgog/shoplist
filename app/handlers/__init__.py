from aiogram import Dispatcher

from handlers import handler
from handlers.states import StateForm


def register_handlers(dp: Dispatcher):
    """
    Register all handlers.
    """
    dp.register_message_handler(handler.start_menu, commands="start")
    dp.register_message_handler(handler.add_product_in_shoplist, state=StateForm.add_product)
    dp.register_message_handler(handler.delete_product_in_shoplist, state=StateForm.delete_product)
    dp.register_message_handler(handler.add_user_in_group, state=StateForm.adding_user)
     

def register_buttons_callback(dp: Dispatcher):
    """
    Register callback for buttons.
    """
    dp.register_callback_query_handler(handler.callback_buttons_handler, lambda callback_query: True)

