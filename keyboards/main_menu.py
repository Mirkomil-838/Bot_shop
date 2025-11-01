from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🧺 Optom"),],
        [KeyboardButton(text="🛒 Savat"), KeyboardButton(text="📦 Buyurtma berish")],
        
    ],
    resize_keyboard=True
)
