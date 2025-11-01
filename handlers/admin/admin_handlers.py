from aiogram import Router, types
from aiogram.filters import Command
from handlers.admin.admin_menu import admin_menu

router = Router()

@router.message(Command("admin"))
async def show_admin_menu(message: types.Message):
    await message.answer("👨‍💼 Admin panelga xush kelibsiz!", reply_markup=admin_menu)
