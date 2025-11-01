from aiogram import Router, types, F
from database.db import get_connection
from config import ADMIN_ID

router = Router()

@router.message(lambda m: m.from_user.id == ADMIN_ID, F.text == "📦 Buyurtmalar")
async def view_orders(message: types.Message):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, user_id, phone, payment, total, created FROM orders ORDER BY id DESC")
    orders = cur.fetchall()
    conn.close()

    if not orders:
        await message.answer("📭 Buyurtmalar mavjud emas.")
        return

    text = "📦 Buyurtmalar ro‘yxati:\n\n"
    for o in orders:
        text += (f"🆔 #{o[0]} | 👤 {o[1]}\n"
                 f"📞 {o[2]}\n"
                 f"💳 {o[3]}\n"
                 f"💰 {o[4]} so‘m\n"
                 f"🕒 {o[5]}\n\n")

    await message.answer(text)
