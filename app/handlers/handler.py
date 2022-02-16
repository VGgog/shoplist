from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers import keyboard, texts, function
from handlers.states import StateForm
from database import shoplist_collection, users_collection, crud


async def start_menu(message: types.Message):
    """
    Send text when user enters the bot first time.
    """
    await message.answer(texts.hello_text)
    await message.answer(texts.group_text, reply_markup=keyboard.group_buttons())


async def callback_buttons_handler(callback_query):
    """
    Callbacks for all buttons.
    """
    await callback_query.message.delete()

    if callback_query.data == "create_group":
        # callback for button whith create a group

        group_id = function.generate_group_id()
        user_id = callback_query.message.chat.id
        
        data = {"_id": group_id, 
                "users": [user_id],
                "shoplist": [],
                }

        crud.create_a_group_doc(shoplist_collection, data)

        await callback_query.message.answer("Группа создана.\n\nКод группы: {}".format(group_id))
        await callback_query.message.answer("Меню:", reply_markup=keyboard.menu_buttons())

    elif callback_query.data == "add_to_a_group":
        # callback whith button for add user in group

        await StateForm.adding_user.set()
        await callback_query.message.answer("Введите код группы:")

    elif callback_query.data == "shoplist":
        await callback_query.message.answer("Меню:", reply_markup=keyboard.menu_buttons())

    elif callback_query.data == "add_to_shoplist":
        await StateForm.add_product.set()
        await callback_query.message.answer("Напишите продукт, который хотите добавить: ")
    
    elif callback_query.data == "delete_in_shoplist":
        await StateForm.delete_product.set()
        await callback_query.message.answer("Введите номер продукта, который хотите удалить: ")


async def add_user_in_group(message: types.Message, state: FSMContext):
    """
    Handler for add user in group 
    """
    text = message.text

    group_id = int(text) if text.isdigit() else text
    data = crud.find_group(shoplist_collection, {"_id": group_id})
    
    if data:    
        users = data["users"]
        users.append(message.chat.id)
        crud.update_document(shoplist_collection, {"_id": group_id}, {"users": users})
        
        await message.answer("Вы добавлены в группу")
        await message.answer("Меню:", reply_markup=keyboard.menu_buttons())
    
    else:
        await message.answer("Группа не найдена")
        await message.answer(texts.group_text, reply_markup=keyboard.group_buttons())
    
    await state.finish()


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

