from aiogram import Router, types
from aiogram.filters import Command
from keyboards.main_menu import main_menu

router = Router()

@router.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "Assalomu alaykum! 🛒\nOnlayn do‘konimizga xush kelibsiz!",
        reply_markup=main_menu
    )
