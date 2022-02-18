from handlers import keyboard, texts, function
from handlers.states import StateForm
from database import shoplist_collection, users_collection, crud


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

        crud.create_document(shoplist_collection, data)

        await callback_query.message.answer("Группа создана.\n\nКод группы: {}".format(group_id))

        # create user info and add this info in users collection
        crud.create_document(users_collection, function.get_data_for_user_collection(group_id, user_id))

        await callback_query.message.answer("Меню:", reply_markup=keyboard.menu_buttons())

    elif callback_query.data == "add_to_a_group":
        # callback whith button for add user in group

        await StateForm.adding_user.set()
        await callback_query.message.answer("Введите код группы:")

    elif callback_query.data == "shoplist":
        # callback button whith display all shoplist

        user_id = callback_query.message.chat.id
        user_info = crud.find_document(users_collection, {"user_id": user_id})
        group_id = user_info["group_id"]

        group_data = crud.find_document(shoplist_collection, {"_id": group_id})
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
        user_info = crud.find_document(users_collection, {"user_id": user_id})
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