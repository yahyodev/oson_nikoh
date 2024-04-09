from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


async def necessary_links_keyboard(telegram_id: int, links_db) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1, inline_keyboard=[])
    for i in links_db:
        btn = InlineKeyboardButton(text=i["title"], url=i["link"])
        markup.inline_keyboard.append([btn])
    return markup
