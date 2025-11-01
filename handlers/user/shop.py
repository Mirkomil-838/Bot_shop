from aiogram import Router, types, F
from database.db import get_connection

from aiogram import types, F, Router

router = Router()

# Kategoriya tanlash bo‘limi
@router.message(F.text.in_(["🧺 Optom", ]))
async def choose_category(message: types.Message):
    markup = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="👞 Erkaklar"), types.KeyboardButton(text="👗 Ayollar")],
            [types.KeyboardButton(text="🧒 Bolalar")],
            [types.KeyboardButton(text="🛒 Savat")],
            [types.KeyboardButton(text="🏠 Asosiy menyuga qaytish")]  # yangi tugma
        ],
        resize_keyboard=True
    )
    await message.answer("🛍️ Kategoriyani tanlang:", reply_markup=markup)


# 🏠 Asosiy menyuga qaytish tugmasi bosilganda
@router.message(F.text == "🏠 Asosiy menyuga qaytish")
async def back_to_main_menu(message: types.Message):
    main_menu = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="🧺 Optom"),types.KeyboardButton(text="🛒 Savat")]
        ],
        resize_keyboard=True
    )
    await message.answer("🏠 Siz asosiy menyuga qaytdingiz. Bo‘limni tanlang:", reply_markup=main_menu)


# 🔹 Kategoriya tanlanganda mahsulotlar ro‘yxatini ko‘rsatish
@router.message(F.text.in_(["👞 Erkaklar", "👗 Ayollar", "🧒 Bolalar"]))
async def show_products(message: types.Message):
    category = message.text.replace("👞 ", "").replace("👗 ", "").replace("🧒 ", "")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, price, description, photo FROM products WHERE category=?", (category,))
    products = cur.fetchall()
    conn.close()

    if not products:
        await message.answer("Bu bo‘limda hozircha mahsulot yo‘q 😔")
        return

    for product_id, name, price, desc, photo in products:
        kb = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text=f"🧺 Savatga qo‘shish", callback_data=f"add_{product_id}")]
        ])
        text = f"📦 <b>{name}</b>\n💰 Narx: {price} so‘m\n📝 {desc}"
        await message.answer_photo(photo=photo, caption=text, reply_markup=kb, parse_mode="HTML")
