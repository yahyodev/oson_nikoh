from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def create_register_keyboard() -> ReplyKeyboardMarkup:
    register_button = KeyboardButton(text="Ro'yxatdan o'tish")
    register_keyboard = ReplyKeyboardMarkup(
        keyboard=[[register_button]],
        resize_keyboard=True,
    )
    return register_keyboard

