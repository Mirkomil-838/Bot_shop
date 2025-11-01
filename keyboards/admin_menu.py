from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Mahsulot qo‘shish")],
        [KeyboardButton(text="📦 Barcha mahsulotlar")],
        [KeyboardButton(text="⬅️ Asosiy menyu")]
    ],
    resize_keyboard=True
)
