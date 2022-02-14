from aiogram import types

from handlers import keyboard


async def start_menu(message: types.Message):
    """
    Send text when user enters the bot first time.
    """
    await message.answer("Приветствую", reply_markup=keyboard.group_buttons())


async def callback_group_buttons_handler(callback_query):
    """
    Callbacks for group buttons.
    """
    if callback_query.data == "create_group":
        print("create_group")
    elif callback_query.data == "add_to_a_group":
        print("add_to_a_group")

