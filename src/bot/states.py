from aiogram.dispatcher.filters.state import State, StatesGroup


class StateForm(StatesGroup):
    add_product = State()
    delete_product = State()
    adding_user = State()
