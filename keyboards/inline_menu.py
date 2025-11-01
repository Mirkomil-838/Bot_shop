from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def category_keyboard():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👞 Erkaklar", callback_data="cat_erkak")],
        [InlineKeyboardButton(text="👠 Ayollar", callback_data="cat_ayol")],
        [InlineKeyboardButton(text="🧒 Bolalar", callback_data="cat_bola")],
    ])
    return kb

def payment_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💵 Naqd", callback_data="pay_cash")],
        [InlineKeyboardButton(text="💳 Karta orqali", callback_data="pay_card")]
    ])
