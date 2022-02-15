from aiogram import types

from handlers import keyboard


async def start_menu(message: types.Message):
    """
    Send text when user enters the bot first time.
    """
    
    await message.answer("Приветствую", reply_markup=keyboard.group_buttons())


async def callback_buttons_handler(callback_query):
    """
    Callbacks for all buttons.
    """
    
    await callback_query.message.delete()

    if callback_query.data == "create_group":
        await callback_query.message.answer("Меню:", reply_markup=keyboard.menu_buttons())

    elif callback_query.data == "add_to_a_group":
        await callback_query.message.answer("Меню:", reply_markup=keyboard.menu_buttons())

    elif callback_query.data == "shoplist":
        await callback_query.message.answer("Меню:", reply_markup=keyboard.menu_buttons())
   
    elif callback_query.data == "add_to_shoplist":
        pass
    
    elif callback_query.data == "delete_in_shoplist":
        pass

