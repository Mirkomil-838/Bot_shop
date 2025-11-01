from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from states.admin_states import AddProduct
from keyboards.admin_menu import admin_menu
from database.db import get_connection
from config import ADMIN_ID

router = Router()

@router.message(lambda m: m.from_user.id == ADMIN_ID, F.text == "➕ Mahsulot qo‘shish")
async def add_product_start(message: types.Message, state: FSMContext):
    await message.answer("Mahsulot turi? (Optom/Dona)")
    await state.set_state(AddProduct.choose_type)

@router.message(AddProduct.choose_type)
async def choose_category(message: types.Message, state: FSMContext):
    await state.update_data(type=message.text.lower())
    await message.answer("Kategoriya kiriting (Erkaklar/Ayollar/Bolalar):")
    await state.set_state(AddProduct.choose_category)

@router.message(AddProduct.choose_category)
async def get_photo(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text.lower())
    await message.answer("Mahsulot rasmi yuboring:")
    await state.set_state(AddProduct.photo)

@router.message(AddProduct.photo, F.photo)
async def get_name(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)
    await message.answer("Mahsulot nomi?")
    await state.set_state(AddProduct.name)

@router.message(AddProduct.name)
async def get_price(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Narxini kiriting:")
    await state.set_state(AddProduct.price)

@router.message(AddProduct.price)
async def get_description(message: types.Message, state: FSMContext):
    await state.update_data(price=float(message.text))
    await message.answer("Mahsulot tavsifini kiriting:")
    await state.set_state(AddProduct.description)

@router.message(AddProduct.description)
async def finish(message: types.Message, state: FSMContext):
    data = await state.get_data()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO products (type, category, name, price, description, image) VALUES (?, ?, ?, ?, ?, ?)",
                (data['type'], data['category'], data['name'], data['price'], data['description'], data['photo']))
    conn.commit()
    conn.close()
    await message.answer("✅ Mahsulot saqlandi!", reply_markup=admin_menu)
    await state.clear()

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from states.product_states import ProductStates
from keyboards.admin_menu import admin_menu
from database.db import get_connection

router = Router()

@router.message(F.text == "➕ Mahsulot qo‘shish")
async def start_add(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text="Optom"), types.KeyboardButton(text="Dona")]],
        resize_keyboard=True
    )
    await message.answer("Mahsulot turi tanlang:", reply_markup=markup)
    await state.set_state(ProductStates.type)

@router.message(ProductStates.type)
async def choose_category(message: types.Message, state: FSMContext):
    await state.update_data(type=message.text)
    markup = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Erkaklar"), types.KeyboardButton(text="Ayollar")],
            [types.KeyboardButton(text="Bolalar")]
        ],
        resize_keyboard=True
    )
    await message.answer("Kategoriya tanlang:", reply_markup=markup)
    await state.set_state(ProductStates.category)

@router.message(ProductStates.category)
async def ask_photo(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text)
    await message.answer("📸 Mahsulot rasmini yuboring:")
    await state.set_state(ProductStates.photo)

@router.message(ProductStates.photo, F.photo)
async def ask_name(message: types.Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    await state.update_data(photo=file_id)
    await message.answer("✏️ Mahsulot nomini kiriting:")
    await state.set_state(ProductStates.name)

@router.message(ProductStates.name)
async def ask_price(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("💰 Mahsulot narxini kiriting:")
    await state.set_state(ProductStates.price)

@router.message(ProductStates.price)
async def ask_description(message: types.Message, state: FSMContext):
    await state.update_data(price=int(message.text))
    await message.answer("📝 Mahsulot tavsifini yozing:")
    await state.set_state(ProductStates.description)

@router.message(ProductStates.description)
async def save_product(message: types.Message, state: FSMContext):
    data = await state.get_data()
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO products (name, price, description, category, type, photo)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (data['name'], data['price'], message.text, data['category'], data['type'], data['photo']))

    conn.commit()
    conn.close()
    await state.clear()
    await message.answer("✅ Mahsulot muvaffaqiyatli qo‘shildi!", reply_markup=admin_menu)
