from aiogram import types


def group_buttons():
    """
    Buttons whith display when user enters bot the first time.
    """
    
    start_menu_keyboard = types.InlineKeyboardMarkup(row_width=1)

    buttons = [
            types.InlineKeyboardButton(text="Создать группу", callback_data="create_group"),
            types.InlineKeyboardButton(text="Добавиться в группу", callback_data="add_to_a_group")]
    
    start_menu_keyboard.add(*buttons)

    return start_menu_keyboard


def menu_buttons():
    """
    Menu buttons to manage the list.
    """

    menu_keyboard = types.InlineKeyboardMarkup(row_width=1)

    buttons = [
            types.InlineKeyboardButton(text="Список", callback_data="shoplist"),
            types.InlineKeyboardButton(text="Добавить в список", callback_data="add_to_shoplist"),
            types.InlineKeyboardButton(text="Удалить из списка", callback_data="delete_in_shoplist")
            ]

    menu_keyboard.add(*buttons)

    return menu_keyboard

