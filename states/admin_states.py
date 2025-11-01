from aiogram.fsm.state import State, StatesGroup

class AddProduct(StatesGroup):
    choose_type = State()
    choose_category = State()
    photo = State()
    name = State()
    price = State()
    description = State()
