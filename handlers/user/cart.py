from aiogram import Router, types, F
from database.db import get_connection

router = Router()

# 🧺 Savatga qo‘shish
@router.callback_query(F.data.startswith("add_"))
async def add_to_cart(callback: types.CallbackQuery):
    product_id = int(callback.data.split("_")[1])
    user_id = callback.from_user.id

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM cart WHERE user_id=? AND product_id=?", (user_id, product_id))
    exists = cur.fetchone()

    if exists:
        cur.execute("UPDATE cart SET quantity = quantity + 1 WHERE user_id=? AND product_id=?", (user_id, product_id))
    else:
        cur.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, 1)", (user_id, product_id))

    conn.commit()
    conn.close()

    await callback.answer("✅ Savatga qo‘shildi!", show_alert=True)


# 🛒 Savatni ko‘rish
@router.message(F.text == "🛒 Savat")
async def view_cart(message: types.Message):
    user_id = message.from_user.id
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT p.name, p.price, c.quantity, p.id 
        FROM cart c 
        JOIN products p ON c.product_id = p.id 
        WHERE c.user_id=?
    """, (user_id,))
    items = cur.fetchall()
    conn.close()

    if not items:
        await message.answer("🛒 Savatingiz bo‘sh.")
        return

    total = 0
    text = "🛍 Savatingizdagi mahsulotlar:\n\n"
    for name, price, qty, pid in items:
        total += price * qty
        text += f"{name} - {price} x {qty} = {price * qty} so‘m\n"

    text += f"\n💰 Jami: {total} so‘m"

    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="❌ Tozalash", callback_data="clear_cart")],
        [types.InlineKeyboardButton(text="📦 Buyurtma berish", callback_data="make_order")]
    ])
    await message.answer(text, reply_markup=kb)


# ❌ Savatni tozalash
@router.callback_query(F.data == "clear_cart")
async def clear_cart(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM cart WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

    await callback.message.answer("🧹 Savat tozalandi.")
    await callback.answer()
