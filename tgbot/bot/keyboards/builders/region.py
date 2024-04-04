from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from tgbot.bot.utils.datas import regions


def get_regions():
    builder = ReplyKeyboardBuilder()

    for txt, _ in regions.items():
        builder.add(KeyboardButton(text=txt))
    builder.adjust(3)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
