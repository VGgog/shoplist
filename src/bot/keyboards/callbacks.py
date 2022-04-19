from aiogram import Dispatcher

from . import keyboard
from .. import functions
from ..states import StateForm
from ..database import shoplist_collection, users_collection, crud


async def callback_buttons_handler(callback_query):
    """
    Callbacks for all buttons.
    """
    await callback_query.message.delete()

    if callback_query.data == "create_group":
        # Callback for button("Создать группу") which create a group.
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

    elif callback_query.data == "add_to_a_group":
        # Callback for button("Присоединиться к группе") for add user in group.
        await StateForm.adding_user.set()
        await callback_query.message.answer("Введите код группы:")

    elif callback_query.data == "shoplist":
        # Callback for button("Список") which display all products in shoplist.
        user_id = callback_query.message.chat.id
        products = functions.get_shoplist(user_id)

        if products:
            user_message = functions.message_which_shopping_list(products)
        else:
            user_message = "Список пуст..."

        await callback_query.message.answer(user_message)
        await callback_query.message.answer("Меню:", reply_markup=keyboard.menu_buttons())

    elif callback_query.data == "add_to_shoplist":
        # Callback for button("Добавить в список") which add new product in shoplist.
        await StateForm.add_product.set()
        await callback_query.message.answer("Напишите продукт, который хотите добавить: ")

    elif callback_query.data == "delete_in_shoplist":
        # Callback for button("Удалить из списка") which delete product in shoplist.
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


def register_buttons_callback(dp: Dispatcher):
    """
    Register callback for buttons.
    """
    dp.register_callback_query_handler(callback_buttons_handler, lambda callback_query: True)
