from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

router = Router()

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔍 Zapchast qidirish")],
        [KeyboardButton(text="➕ Zapchast qo'shish")],
        [KeyboardButton(text="📋 Barcha zapchastlar")]

    ],
    resize_keyboard=True
)


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f"Assalomu alaykum, {message.from_user.first_name}! 👋\n\n"
        "Isuzu zapchastlar bazasiga xush kelibsiz.\n"
        "Quyidagi tugmalardan birini tanlang:",
        reply_markup=main_menu
    )