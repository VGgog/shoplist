from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher

from states import StateForm
from keyboards import keyboard
import texts
import functions
from database import shoplist_collection, users_collection, crud


async def menu(message: types.Message):
    """
    The bot's response to the start command.
    """
    user_id = message.chat.id

    if crud.find_document(users_collection, {"user_id": user_id}):
        # If user is in the users collection then he consist in group.
        # And so that the user don't add in other group he get menu buttons.
        await message.answer("Меню:", reply_markup=keyboard.menu_buttons())
    else:
        # If user not in users collection then he gets group buttons. 
        # For add to group or create group.
        await message.answer(texts.group_text, reply_markup=keyboard.group_buttons())


async def add_user_in_group(message: types.Message, state: FSMContext):
    """
    Handler for add user in group.
    """
    text = message.text
    user_id = message.chat.id
    group_id = int(text) if text.isdigit() else text
    data = crud.find_document(shoplist_collection, {"_id": group_id})

    if data:    
        # Add new user in shoplist_collection.
        users = data["users"]
        users.append(user_id)
        crud.update_document(shoplist_collection, {"_id": group_id}, {"users": users})
        await message.answer("Вы добавлены в группу.")
        
        # Create and add new user in users_collection.
        crud.create_document(users_collection, functions.get_data_for_users_collection(group_id, user_id))
        await message.answer("Меню:", reply_markup=keyboard.menu_buttons())
    else:
        await message.answer("Группа не найдена.")
        await message.answer(texts.group_text, reply_markup=keyboard.group_buttons())
    
    await state.finish()


async def add_product_in_shoplist(message: types.Message, state: FSMContext):
    """
    Handler for add product in shoplist.
    """
    product = message.text
    user_id = message.chat.id

    group_id = functions.get_group_id(user_id)
    products = functions.get_shoplist(user_id)
    products.append(product)

    crud.update_document(shoplist_collection, {"_id": group_id}, {"shoplist": products})

    await message.answer("Продукт добавлен.")

    await state.finish()
    await message.answer("Меню:", reply_markup=keyboard.menu_buttons())


async def delete_product_in_shoplist(message: types.Message, state: FSMContext):
    """
    Handler for delete product in shoplist. 
    """
    product_text = message.text

    if product_text.isdigit():
        product_index = int(product_text)
        user_id = message.chat.id
        group_id = functions.get_group_id(user_id)
        products = functions.get_shoplist(user_id)

        if product_index in range(1, len(products) + 1):
            products.pop(product_index - 1)
            crud.update_document(shoplist_collection, {"_id": group_id}, {"shoplist": products})
            await message.answer("Продукт удалён.")
        else:
            await message.answer("Такого пункта нет...")
    
    else:
        await message.answer("Введите число:")
    
    await state.finish()
    await message.answer("Меню:", reply_markup=keyboard.menu_buttons())


async def send_group_code(message: types.Message):
    """
    Handler for send user code group.
    """
    user_id = message.chat.id
    user_info = crud.find_document(users_collection, {"user_id": user_id})
    
    if user_info:
        group_id = user_info["group_id"]

        await message.answer("Код группы:\n\n{}".format(group_id))
        await message.answer("Меню:", reply_markup=keyboard.menu_buttons())
    else:
        await message.answer("Вы не состоите в группе.")
        await message.answer(texts.group_text, reply_markup=keyboard.group_buttons())


async def exit_group(message: types.Message):
    """
    Handler for exit in group.
    """
    user_id = message.chat.id
    user_data = {"user_id": user_id}
    user_info = crud.find_document(users_collection, user_data)

    if user_info:
        group_id = user_info["group_id"]
        group_data = {"_id": group_id}
        
        # Delete user in users collection.
        crud.delete_document(users_collection, user_data)
        
        users = crud.find_document(shoplist_collection, group_data)
        users_list = users["users"]
        users_list.remove(user_id)

        # Delete user in users list in shoplist collection.
        crud.update_document(shoplist_collection, group_data, {"users": users_list})
        
        await message.answer("Вы вышли из группы.")
    else:
        await message.answer("Вы не состоите в группе.")
    
    await message.answer(texts.group_text, reply_markup=keyboard.group_buttons())


async def answer_other_message(message: types.Message):
    """
    Handler for answer users message.
    """
    await message.answer("Я не умею читать...")
    await menu(message)


def register_handlers(dp: Dispatcher):
    """
    Register all handlers.
    """
    dp.register_message_handler(menu, content_types=["text"], commands=["start", "menu"])
    dp.register_message_handler(send_group_code, commands="code")
    dp.register_message_handler(exit_group, commands="exit")

    dp.register_message_handler(answer_other_message)

    dp.register_message_handler(add_product_in_shoplist, state=StateForm.add_product)
    dp.register_message_handler(delete_product_in_shoplist, state=StateForm.delete_product)
    dp.register_message_handler(add_user_in_group, state=StateForm.adding_user)
