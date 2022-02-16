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
        data = {
                "group_id": group_id,
                "user_id": user_id
                }

        crud.create_a_group_doc(users_collection, data)

        await callback_query.message.answer("Меню:", reply_markup=keyboard.menu_buttons())

    elif callback_query.data == "add_to_a_group":
        # callback whith button for add user in group

        await StateForm.adding_user.set()
        await callback_query.message.answer("Введите код группы:")

    elif callback_query.data == "shoplist":
       
        user_id = callback_query.message.chat.id
        user_info = crud.find_group(users_collection, {"user_id": user_id})
        group_id = user_info["group_id"]
        
        group_data = crud.find_group(shoplist_collection, {"_id": group_id})
        products = group_data["shoplist"]
       
        if products:
            i = 1
            user_message = ''
            for product in products:
                user_message += "{}) {}\n".format(i, product)
                i += 1

        else:
            user_message = "Список пуст..."

        await callback_query.message.answer(user_message)
        await callback_query.message.answer("Меню:", reply_markup=keyboard.menu_buttons())

    elif callback_query.data == "add_to_shoplist":
        await StateForm.add_product.set()
        await callback_query.message.answer("Напишите продукт, который хотите добавить: ")
    
    elif callback_query.data == "delete_in_shoplist":
        user_id = callback_query.message.chat.id
        user_info = crud.find_group(users_collection, {"user_id": user_id})
        group_id = user_info["group_id"]

        group_data = crud.find_group(shoplist_collection, {"_id": group_id})
        products = group_data["shoplist"]

        if products:
            i = 1
            user_message = ''
            for product in products:
                user_message += "{}) {}\n".format(i, product)
                i += 1
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
        data = {
                "group_id": group_id,
                "user_id": user_id
                }

        crud.create_a_group_doc(users_collection, data)

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

    group_data = crud.find_group(shoplist_collection, {"_id": group_id})
    products = group_data["shoplist"]
    
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

        group_data = crud.find_group(shoplist_collection, {"_id": group_id})
        products = group_data["shoplist"]

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

