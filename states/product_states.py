from aiogram.fsm.state import StatesGroup, State

class ProductStates(StatesGroup):
    type = State()
    category = State()
    photo = State()
    name = State()
    price = State()
    description = State()
