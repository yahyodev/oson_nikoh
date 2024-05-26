from typing import Union

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message

from tgbot.bot.utils.db_api import db_commands


async def start_keyboard(
        obj: Union[CallbackQuery, Message, int]
) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[], row_width=1, one_time_keyboard=True)

    status = False
    user_db = None
    if isinstance(obj, Message):
        user_db = await db_commands.select_user(obj.from_user.id)
    elif isinstance(obj, CallbackQuery):
        user_db = await db_commands.select_user(obj.message.from_user.id)
    elif isinstance(obj, int):
        user_db = await db_commands.select_user(obj)

    if user_db is not None:
        status = user_db.status

    registration = InlineKeyboardButton(
        text="📄Ro'yxatdan o'tish", callback_data="registration"
    )
    my_profile = InlineKeyboardButton(
        text="👤Mening anketam", callback_data="my_profile"
    )
    # filters = InlineKeyboardButton(text="⚙️ Yoshga talablar", callback_data="filters")
    view_ques = InlineKeyboardButton(text="💌 Anketalarni ko'rish", callback_data="find_ques")
    if not status:
        markup.inline_keyboard.append([registration])
    else:
        markup.inline_keyboard.append([my_profile])
        markup.inline_keyboard.append([view_ques])
        # markup.inline_keyboard.append([filters])
    return markup
