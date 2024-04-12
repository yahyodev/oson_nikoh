import random
import secrets
from typing import (
    List, Union,
)

from asgiref.sync import sync_to_async
from async_lru import alru_cache
from aiogram.types import CallbackQuery, Message, KeyboardButton, ReplyKeyboardMarkup

from tgbot.bot.utils.db_api import (
    db_commands,
)
from tgbot.models import User, ViewedProfile


# @alru_cache(ttl=1800)
async def get_next_user(
        telegram_id: int
) -> List[int]:
    user = await db_commands.select_user(telegram_id)

    # viewed_profiles_ids = await db_commands.get_user_profiles(user)

    user_filter = await db_commands.search_users(
        sex=user.sex,
        location=user.location,
        age=user.age,
        telegram_id=user.telegram_id,
        need_age_min=user.need_partner_age_min,
        need_age_max=user.need_partner_age_max
    )

    if len(user_filter) < 30:
        user_filter = await db_commands.search_users(
            sex=user.sex,
            age=user.age,
            telegram_id=user.telegram_id,
            need_age_min=user.need_partner_age_min,
            need_age_max=user.need_partner_age_max
        )

    if len(user_filter) < 30:
        user_filter = await db_commands.search_users(
            sex=user.sex,
            telegram_id=user.telegram_id,
        )

    return user_filter


async def rand_user_list(telegram_id) -> Union[int, None]:
    user_list = await get_next_user(telegram_id)
    try:
        random_user_list = [random.choice(user_list) for _ in range(len(user_list))]
        random_user = secrets.choice(random_user_list)
        return random_user
    except IndexError:
        return None


async def create_que(telegram_id: int, obj: Union[CallbackQuery, Message]):
    user = await db_commands.select_user(telegram_id)

    user_info_template = "{sex_emoji}{name}, {age}, {location}, \n\n" \
                         "📊{height} sm - {weight} kg\n\n" \
                         "🇺🇳Millati: {ethnicity}\n\n" \
                         "👨‍👩‍👧‍👦Oilaviy holati: {marital_status}\n\n" \
                         "{edu_emoji}Ma'lumoti: {education}\n\n" \
                         "💵Kasbi: {occupation}\n\n" \
                         "{sex_emoji_2}{partner}ni yosh chegarasi: {min_age}-{max_age}\n\n" \
                         "💢O'zi haqida: {biography}"

    sex_emoji = "🤵‍♂" if user.sex == 'erkak' else '👰‍♀'
    sex_emoji_2 = '🤵‍♂' if user.sex == 'ayol' else "👰‍♀"
    edu_emoji = "👨‍🎓" if user.sex == 'erkak' else '👩‍🎓'
    partner = "kelin" if user.sex == "erkak" else "kuyov"
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
        biography=user.biography,
        partner=partner.capitalize(),
        min_age=user.need_partner_age_min,
        max_age=user.need_partner_age_max,
        sex_emoji_2=sex_emoji_2
    )

    kb = [
        [
            KeyboardButton(text="👍"),
            KeyboardButton(text="👎"),
            KeyboardButton(text="shikoyat"),
            KeyboardButton(text="🔙")
        ],
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Qaysidir tugmani tanlang..."
    )

    if isinstance(obj, CallbackQuery):
        obj = obj.message
    await obj.answer_photo(
        caption=user_info[:1023], photo=user.photo_id, reply_markup=keyboard
    )
