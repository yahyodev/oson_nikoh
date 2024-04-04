import asyncio
from typing import Union

from aiogram import Bot
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message, KeyboardButton, ReplyKeyboardMarkup, Update

from tgbot.bot.utils.db_api import db_commands


async def display_profile(obj: Update,
                          markup: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup] = None) -> None:
    """Function for displaying the user profile."""
    await asyncio.sleep(1)
    if isinstance(obj, CallbackQuery):
        obj = obj.message.chat
    user = await db_commands.select_user(obj.chat.id)

    user_info_template = "{sex_emoji}{name}, {age}, {location}, \n\n" \
                         "📊{height} sm - {weight} kg\n\n" \
                         "🇺🇳Millati: {ethnicity}\n\n" \
                         "👨‍👩‍👧‍👦Oilaviy holati: {marital_status}\n\n" \
                         "{edu_emoji}Ma'lumoti: {education}\n\n" \
                         "💵Kasbi: {occupation}\n\n" \
                         "💢O'zi haqida: {biography}"

    sex_emoji = "🤵‍♂" if user.sex == 'erkak' else '👰‍♀'
    edu_emoji = "👨‍🎓" if user.sex == 'erkak' else '👩‍🎓'
    user_info = user_info_template.format(
        sex_emoji=sex_emoji,
        edu_emoji=edu_emoji,
        name=user.name,
        age=user.age,
        location=user.location,
        height=user.height,
        weight=user.weight,
        ethnicity=user.ethnicity,
        marital_status=user.marital_status,
        education=user.education,
        occupation=user.occupation,
        biography=user.biography
    )

    await obj.answer_photo(
        caption=user_info, photo=user.photo_id
    )


async def profile_choices(obj: Union[CallbackQuery, Message]):
    await asyncio.sleep(1)
    text = "1. Anketalarni ko'rish\n" \
           "2. Anketamni butunlay yoki qisman o'zgartirish\n" \
           "3. Anketamni olib tashlash\n" \
           "4. Mening anketam\n" \
           "5. Yoshga talablar"

    if isinstance(obj, CallbackQuery):
        obj = obj.message

    kb = [
        [
            KeyboardButton(text="1🚀"),
            KeyboardButton(text="2"),
            KeyboardButton(text="3"),
            KeyboardButton(text="4"),
            KeyboardButton(text="5")
        ],
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Qaysidir tugmani tanlang..."
    )
    await obj.answer(text,
                     reply_markup=keyboard)
