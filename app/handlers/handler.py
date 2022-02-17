from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers import keyboard, texts, function
from handlers.states import StateForm
from database import shoplist_collection, users_collection, crud


async def start_menu(message: types.Message):
    """
    The bot's response to the start command.
    """
    await message.answer(texts.hello_text)
    
    user_id = message.chat.id
    
    if crud.find_group(users_collection, {"user_id": user_id}):
        # If user is in the users collection then he consist in group.
        # And so that the user don't add in other group he get menu buttons.
        
        await message.answer("Меню:", reply_markup=keyboard.menu_buttons())
    
    else:
        # If user not in users collection then he gets group buttons. 
        # For add to group or create group.

        await message.answer(texts.group_text, reply_markup=keyboard.group_buttons())


async def callback_buttons_handler(callback_query):
    """
    Callbacks for all buttons.
    """
    await callback_query.message.delete()

    # callback for button whith create a group
    if callback_query.data == "create_group":

        group_id = function.generate_group_id()
        user_id = callback_query.message.chat.id
        
        # create group info and add this info in shoplist collection
        data = {
                "_id": group_id, 
                "users": [user_id],
                "shoplist": [],
                }

        crud.create_a_group_doc(shoplist_collection, data)

        await callback_query.message.answer("Группа создана.\n\nКод группы: {}".format(group_id))
        
        # create user info and add this info in users collection
        crud.create_a_group_doc(users_collection, function.get_data_for_user_collection(group_id, user_id))

        await callback_query.message.answer("Меню:", reply_markup=keyboard.menu_buttons())

    elif callback_query.data == "add_to_a_group":
        # callback whith button for add user in group

        await StateForm.adding_user.set()
        await callback_query.message.answer("Введите код группы:")

    elif callback_query.data == "shoplist":
        # callback button whith display all shoplist

        user_id = callback_query.message.chat.id
        user_info = crud.find_group(users_collection, {"user_id": user_id})
        group_id = user_info["group_id"]
        
        group_data = crud.find_group(shoplist_collection, {"_id": group_id})
        products = group_data["shoplist"]
       
        if products:
            user_message = function.get_user_message(products)
        else:
            user_message = "Список пуст..."

        await callback_query.message.answer(user_message)
        await callback_query.message.answer("Меню:", reply_markup=keyboard.menu_buttons())

    elif callback_query.data == "add_to_shoplist":
        # callback buttons for add new product in shoplist

        await StateForm.add_product.set()
        await callback_query.message.answer("Напишите продукт, который хотите добавить: ")
    
    elif callback_query.data == "delete_in_shoplist":
        # callback buttons for delete product in shoplist

        user_id = callback_query.message.chat.id
        user_info = crud.find_group(users_collection, {"user_id": user_id})
        group_id = user_info["group_id"]

        products = function.get_shoplist(group_id)

        if products:
            user_message = function.get_user_message(products)
            await callback_query.message.answer(user_message)
            await StateForm.delete_product.set()
            await callback_query.message.answer("Введите номер продукта, который хотите удалить: ")

        else:
            await callback_query.message.answer("Список пуст...")
            await callback_query.message.answer("Меню:", reply_markup=keyboard.menu_buttons())


async def add_user_in_group(message: types.Message, state: FSMContext):
    """
    Handler for add user in group 
    """
    text = message.text

    group_id = int(text) if text.isdigit() else text
    data = crud.find_group(shoplist_collection, {"_id": group_id})
    user_id = message.chat.id

    if data:    
        # add new user in shoplist collection
        users = data["users"]
        users.append(user_id)
        crud.update_document(shoplist_collection, {"_id": group_id}, {"users": users})
        
        await message.answer("Вы добавлены в группу")
        
        # create and add new user in users collection
        crud.create_a_group_doc(users_collection, function.get_data_for_user_collection(group_id, user_id))

        await message.answer("Меню:", reply_markup=keyboard.menu_buttons())
    
    else:
        await message.answer("Группа не найдена")
        await message.answer(texts.group_text, reply_markup=keyboard.group_buttons())
    
    await state.finish()


async def add_product_in_shoplist(message: types.Message, state: FSMContext):
    """
    Handler for add product in shoplist.
    """
    product_text = message.text

    user_id = message.chat.id
    user_info = crud.find_group(users_collection, {"user_id": user_id})
    group_id = user_info["group_id"]

    products = function.get_shoplist(group_id)

    products.append(product_text)
    crud.update_document(shoplist_collection, {"_id": group_id}, {"shoplist": products})

    await message.answer("Продукт добавлен")
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
        user_info = crud.find_group(users_collection, {"user_id": user_id})
        group_id = user_info["group_id"]

        products = function.get_shoplist(group_id)

        if product_index in range(1, len(products) + 1):
            products.pop(product_index - 1)
            crud.update_document(shoplist_collection, {"_id": group_id}, {"shoplist": products})
            await message.answer("Продукт удалён")
        else:
            await message.answer("Такого пункта нет")
    
    else:
        await message.answer("Введите число")
    
    await state.finish()
    await message.answer("Меню:", reply_markup=keyboard.menu_buttons())


async def send_group_code(message: types.Message):
    """
    Handler for send user code group
    """
    user_id = message.chat.id
    user_info = crud.find_group(users_collection, {"user_id": user_id})
    
    if user_info:
        group_id = user_info["group_id"]
        
        await message.answer("Код группы:\n\n{}".format(group_id))
        await message.answer("Меню:", reply_markup=keyboard.menu_buttons())

    else:
        await message.answer("Вы не состоите в группе")
        await message.answer(texts.group_text, reply_markup=keyboard.group_buttons())


async def exit_group(message: types.Message):
    """
    Handler for exit user in group
    """
    user_id = message.chat.id
    user_data = {"user_id": user_id}
    user_info = crud.find_group(users_collection, user_data)

    if user_info:
        group_id = user_info["group_id"]
        group_data = {"_id": group_id}
        
        # Delete user in users collection
        crud.delete_document(users_collection, user_data)
        
        users = crud.find_group(shoplist_collection, group_data)
        users_list = users["users"]
        users_list.remove(user_id)

        # Delete user in users list in shoplist collection
        crud.update_document(shoplist_collection, group_data, {"users": users_list})
        
        await message.answer("Вы вышли из группы")

    else:
        await message.answer("Вы не состоите в группе")
    
    await message.answer(texts.group_text, reply_markup=keyboard.group_buttons())

