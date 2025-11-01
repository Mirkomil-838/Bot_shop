from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = Router()

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Mahsulot qo‘shish")],
        [KeyboardButton(text="📦 Buyurtmalarni ko‘rish")],
        [KeyboardButton(text="🔙 Asosiy menyuga qaytish")]
    ],
    resize_keyboard=True
)

@router.message(Command("admin"))
async def show_admin_menu(message: types.Message):
    await message.answer("👨‍💼 Admin panelga xush kelibsiz!", reply_markup=admin_menu)
