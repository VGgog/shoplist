import functions
from states import StateForm
from database import shoplist_collection, users_collection, crud
from keyboards import keyboard


async def callback_buttons_handler(callback_query):
    """
    Callbacks for all buttons.
    """
    await callback_query.message.delete()

    # Callback for button("Создать группу") which create a group.
    if callback_query.data == "create_group":

        group_id = functions.generate_group_id()
        user_id = callback_query.message.chat.id

        # Create group info and add this info in shoplist_collection.
        data = {
            "_id": group_id,
            "users": [user_id],
            "shoplist": [],
        }
        crud.create_document(shoplist_collection, data)

        await callback_query.message.answer("Группа создана.\n\nКод группы: {}".format(group_id))

        # Create user info and add this info in users_collection.
        crud.create_document(users_collection, functions.get_data_for_users_collection(group_id, user_id))

        await callback_query.message.answer("Меню:", reply_markup=keyboard.menu_buttons())

    # Callback for button("Присоединиться к группе") for add user in group.
    elif callback_query.data == "add_to_a_group":

        await StateForm.adding_user.set()
        await callback_query.message.answer("Введите код группы:")

    # Callback for button("Список") which display all products in shoplist.
    elif callback_query.data == "shoplist":

        user_id = callback_query.message.chat.id
        products = functions.get_shoplist(user_id)

        if products:
            user_message = functions.message_which_shopping_list(products)

        else:
            user_message = "Список пуст..."

        await callback_query.message.answer(user_message)
        await callback_query.message.answer("Меню:", reply_markup=keyboard.menu_buttons())

    # Callback for button("Добавить в список") which add new product in shoplist.
    elif callback_query.data == "add_to_shoplist":

        await StateForm.add_product.set()
        await callback_query.message.answer("Напишите продукт, который хотите добавить: ")

    # Callback for button("Удалить из списка") which delete product in shoplist.
    elif callback_query.data == "delete_in_shoplist":

        user_id = callback_query.message.chat.id
        products = functions.get_shoplist(user_id)

        if products:
            # Send message with numbered list with all products.
            user_message = functions.message_which_shopping_list(products)
            await callback_query.message.answer(user_message)

            await StateForm.delete_product.set()
            await callback_query.message.answer("Введите номер продукта, который хотите удалить: ")

        else:
            await callback_query.message.answer("Список пуст...")
            await callback_query.message.answer("Меню:", reply_markup=keyboard.menu_buttons())
