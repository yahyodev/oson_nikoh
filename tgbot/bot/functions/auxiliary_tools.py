import asyncio
from typing import Union

from aiogram import Bot
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message, KeyboardButton, ReplyKeyboardMarkup, Update, \
    InlineKeyboardButton

from tgbot.bot.utils.db_api import db_commands


async def display_profile(obj: Update,
                          markup: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup] = None) -> None:
    """Function for displaying the user profile."""
    if isinstance(obj, CallbackQuery):
        obj = obj.message.chat
    user = await db_commands.select_user(obj.chat.id)

    user_info_template = "{sex_emoji}{name}, {age}, {location}, \n\n" \
                         "📊{height} sm - {weight} kg\n\n" \
                         "🇺🇳Millati: {ethnicity}\n\n" \
                         "👨‍👩‍👧‍👦Oilaviy holati: {marital_status}\n\n" \
                         "{edu_emoji}Ma'lumoti: {education}\n\n" \
                         "💵Kasbi: {occupation}\n\n" \
                         "{sex_emoji_2}{partner}ni yosh chegarasi: {min_age}-{max_age}\n\n" \
                         "💢O'zi haqida va talablari: {biography}"

    sex_emoji = "🤵‍♂" if user.sex == 'erkak' else '👰‍♀'
    sex_emoji_2 = '🤵‍♂' if user.sex == 'ayol' else "👰‍♀"
    edu_emoji = "👨‍🎓" if user.sex == 'erkak' else '👩‍🎓'
    partner = "kelin" if user.sex == 'erkak' else 'kuyov'

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

    await obj.answer_photo(
        caption=user_info[:1023], photo=user.photo_id
    )


async def profile_choices(obj: Union[CallbackQuery, Message]):
    text = "1. Anketalarni ko'rish\n" \
           "2. Anketamni butunlay yoki qisman o'zgartirish\n" \
           "3. Anketamni olib tashlash\n" \
           "4. Mening anketam"

    if isinstance(obj, CallbackQuery):
        obj = obj.message

    kb = [
        [
            KeyboardButton(text="1🚀"),
            KeyboardButton(text="2"),
            KeyboardButton(text="3"),
            KeyboardButton(text="4"),
        ],
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Qaysidir tugmani tanlang..."
    )
    await obj.answer(text,
                     reply_markup=keyboard)


async def send_profile(obj: Message, telegram_id: int, bot: Bot) -> None:
    """Function for displaying the user profile."""
    # await asyncio.sleep(0.1)

    user = await db_commands.select_user(obj.from_user.id)

    user_info_template = ("👀Kimdir sizni e'lonizga qiziqdi:\n\n"
                          "{sex_emoji}{name}, {age}, {location}, \n\n" \
                          "📊{height} sm - {weight} kg\n\n" \
                          "🇺🇳Millati: {ethnicity}\n\n" \
                          "👨‍👩‍👧‍👦Oilaviy holati: {marital_status}\n\n" \
                          "{edu_emoji}Ma'lumoti: {education}\n\n" \
                          "💵Kasbi: {occupation}\n\n" \
                          "{sex_emoji_2}{partner}ni yosh chegarasi: {min_age}-{max_age}\n\n" \
                          "💢O'zi haqida va talablari: {biography}")

    sex_emoji = "🤵‍♂" if user.sex == 'erkak' else '👰‍♀'
    edu_emoji = "👨‍🎓" if user.sex == 'erkak' else '👩‍🎓'
    sex_emoji_2 = '🤵‍♂' if user.sex == 'ayol' else "👰‍♀"
    partner = "kelin" if user.sex == 'erkak' else 'kuyov'
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

    markup = InlineKeyboardMarkup(inline_keyboard=[], one_time_keyboard=True)
    like = InlineKeyboardButton(
        text="👍Akkauntni olish", callback_data=f"like_{telegram_id}_{obj.from_user.id}"
    )
    dislike = InlineKeyboardButton(
        text="👎Keyingisi", callback_data=f"dislike"
    )

    markup.inline_keyboard.append([like])
    markup.inline_keyboard.append([dislike])
    # print('hiiii', telegram_id, user.telegram_id)
    await bot.send_photo(chat_id=telegram_id,
                         caption=user_info[:1023],
                         photo=user.photo_id,
                         reply_markup=markup
                         )


# async def start_texting(liked_id: int, liker_id: int, bot: Bot):
#     from aiogram import types
#     liker = await db_commands.select_user(liker_id)
#     liked = await db_commands.select_user(liked_id)
#     liker_user = types.User(id=liker_id)
#     liked_user = types.User(id=liked_id)
#     await bot.send_message(chat_id=liked_id,
#                            text=f"{liker.name}  {liker.age}  {liker.location}'ning akkaunti uchun <a href='{liker_user.get_mention(as_html=True)}'>bu yerga bosing</a>")
#     await bot.send_message(chat_id=liker_id,
#                            text=f"{liked.name}  {liked.age}  {liked.location}'ning akkaunti uchun <a href='{liked_user.get_mention(as_html=True)}'>bu yerga bosing</a>")

async def start_texting(call: CallbackQuery, liker_id: int, liked_id: int, bot: Bot):
    user = await db_commands.select_user(liked_id)

    user_info_template = ("👍Siz layk bosgan odam sizga qaytib layk bosdi:\n\n"
                          "{sex_emoji}{name}, {age}, {location}, \n\n" \
                          "📊{height} sm - {weight} kg\n\n" \
                          "🇺🇳Millati: {ethnicity}\n\n" \
                          "👨‍👩‍👧‍👦Oilaviy holati: {marital_status}\n\n" \
                          "{edu_emoji}Ma'lumoti: {education}\n\n" \
                          "💵Kasbi: {occupation}\n\n" \
                          "💢O'zi haqida: {biography}\n\n" \
                          "🔗Akkaunt uchun <a href='tg://user?id={liked_id}'>{username}</a>")
    if user.phone_number:
        user_info_template += "\nAgar ishlamasa <a href='https://t.me/{number}'>qo'shimcha ssilka</a>"
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
        biography=user.biography,
        liked_id=liked_id,
        username=('bu yerga bosing' if not user.username else '@' + user.username),
        number="+" + str(user.phone_number)
    )

    await bot.send_photo(photo=user.photo_id,
                         caption=user_info[:1023],
                         chat_id=liker_id
                         )
