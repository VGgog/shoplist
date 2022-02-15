from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers import keyboard
from handlers.states import StateForm

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
        await StateForm.add_product.set()
        await callback_query.message.answer("Напишите продукт, который хотите добавить: ")
    
    elif callback_query.data == "delete_in_shoplist":
        await StateForm.delete_product.set()
        await callback_query.message.answer("Введите номер продукта, который хотите удалить: ")


async def add_product_in_shoplist(message: types.Message, state: FSMContext):
    """
    Handler for add product in shoplist.
    """
    await message.answer("Продукт добавлен")
    await state.finish()
    await message.answer("Меню:", reply_markup=keyboard.menu_buttons())


async def delete_product_in_shoplist(message: types.Message, state: FSMContext):
    """
    Handler for delete product in shoplist. 
    """
    await message.answer("Продукт удалён")
    await state.finish()
    await message.answer("Меню:", reply_markup=keyboard.menu_buttons())

