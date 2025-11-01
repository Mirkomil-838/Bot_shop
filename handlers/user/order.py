from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from states.order_states import OrderStates
from keyboards.inline_menu import payment_keyboard
from config import ADMIN_ID
from database.db import get_connection

router = Router()

@router.callback_query(F.data == "make_order")
async def start_order(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("📞 Telefon raqamingizni kiriting:")
    await state.set_state(OrderStates.phone)
    await callback.answer()

@router.message(OrderStates.phone)
async def get_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("📍 Joylashuvingizni yuboring (Share Location tugmasini bosing).", reply_markup=
        types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton(text="📍 Joylashuvni yuborish", request_location=True)]],
            resize_keyboard=True
        )
    )
    await state.set_state(OrderStates.location)

@router.message(OrderStates.location, F.location)
async def get_payment(message: types.Message, state: FSMContext):
    lat = message.location.latitude
    lon = message.location.longitude
    await state.update_data(location=f"{lat},{lon}")
    await message.answer("💳 To‘lov turini tanlang:", reply_markup=payment_keyboard())
    await state.set_state(OrderStates.payment)

@router.callback_query(OrderStates.payment)
async def finish_order(callback: types.CallbackQuery, state: FSMContext):
    payment_type = "Naqd" if callback.data == "pay_cash" else "Karta"
    await state.update_data(payment=payment_type)
    data = await state.get_data()
    user_id = callback.from_user.id

    conn = get_connection()
    cur = conn.cursor()

    # Savatdan jami summani hisoblash
    cur.execute("""
        SELECT SUM(p.price * c.quantity) 
        FROM cart c JOIN products p ON c.product_id = p.id 
        WHERE c.user_id=?
    """, (user_id,))
    total = cur.fetchone()[0] or 0

    cur.execute("INSERT INTO orders (user_id, phone, location, payment, total) VALUES (?, ?, ?, ?, ?)",
                (user_id, data['phone'], data['location'], data['payment'], total))
    conn.commit()

    # Admin uchun xabar
    await callback.bot.send_message(
        ADMIN_ID,
        f"📦 Yangi buyurtma!\n\n👤 ID: {user_id}\n📞 Tel: {data['phone']}\n📍 Lokatsiya: {data['location']}\n💳 To‘lov: {data['payment']}\n💰 Jami: {total} so‘m"
    )

    # Savatni tozalash
    cur.execute("DELETE FROM cart WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

    await callback.message.answer("✅ Buyurtmangiz qabul qilindi! Tez orada siz bilan bog‘lanamiz.")
    await state.clear()
