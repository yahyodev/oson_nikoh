from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def request_contact() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text="Kontaktni so'rash", request_contact=True),
        ],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb,
                                   one_time_keyboard=True,
                                   resize_keyboard=True)

    return keyboard
