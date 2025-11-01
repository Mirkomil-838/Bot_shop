from aiogram import Router, types
from aiogram.filters import Command
from config import ADMIN_ID
from keyboards.admin_menu import admin_menu

router = Router()

@router.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Sizda admin panelga kirish huquqi yo‘q.")
        return
    
    await message.answer(
        "👑 Admin panelga xush kelibsiz!\nQuyidagi amallardan birini tanlang:",
        reply_markup=admin_menu
    )
