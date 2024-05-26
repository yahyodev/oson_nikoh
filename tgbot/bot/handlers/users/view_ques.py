import asyncio
from typing import Union

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from tgbot.bot.functions.auxiliary_tools import (
    profile_choices,
    send_profile,
    start_texting,
    send_profile_premium)
from tgbot.bot.functions.dating import rand_user_list, create_que
from tgbot.bot.loader import bot
from django.conf import settings

from tgbot.models import User
from tgbot.bot.utils.db_api import db_commands
from tgbot.bot.states import RegData, SearchQues, ChangeData
from tgbot.bot.keyboards.inline import start_keyboard
from tgbot.bot.functions.common import update_user_data

router = Router()


@router.callback_query(F.data == "find_ques")
@router.message(SearchQues.profile_options, F.text == "1🚀")
@router.message(ChangeData.start, F.text == "1🚀")
@router.message(SearchQues.viewing_ques, F.text == "Anketalarni ko'rish")
async def find_ques(obj: Union[CallbackQuery, Message], state: FSMContext) -> None:
    telegram_id = obj.from_user.id
    if isinstance(obj, CallbackQuery):
        telegram_id = obj.message.chat.id
    await state.set_state(SearchQues.viewing_ques)
    await update_user_data(telegram_id, active=True)

    if isinstance(obj, CallbackQuery):
        obj = obj.message

    user = await rand_user_list(telegram_id)
    if user is None:
        await obj.answer("Uzr hozirchalik sizga mos odam topilmadi,\n"
                         "Adminga yozib ko'ring")
    else:
        await state.update_data(last_profile_user_id=user)
        await create_que(user, obj)


@router.message(SearchQues.viewing_ques, F.text == "👍")
async def like_que(message: Message, state: FSMContext, bot: Bot) -> None:
    data = await state.get_data()
    data = data.get('last_profile_user_id')

    await update_user_data(telegram_id=message.from_user.id,
                           username=message.from_user.username)

    user = await db_commands.select_user(int(data))
    real_user = await db_commands.select_user(telegram_id=message.from_user.id)

    if user and user.is_fake or real_user.premium:
        first_sentence = "💸Bizga sodiq bo'lganiz uchun " \
                         "bu bonus akkaunt\n\n" if user.is_fake else "💵Premium bo'lganiz uchun bu sizga bu anketa\n\n"
        user_info_template = (
                first_sentence +
                "{sex_emoji}{name}, {age}, {location}, \n\n" \
                "📊{height} sm - {weight} kg\n\n" \
                "🇺🇳Millati: {ethnicity}\n\n" \
                "👨‍👩‍👧‍👦Oilaviy holati: {marital_status}\n\n" \
                "{edu_emoji}Ma'lumoti: {education}\n\n" \
                "💵Kasbi: {occupation}\n\n" \
                "💢O'zi haqida: {biography}\n\n" \
                "🔗Akkaunt uchun <a href='tg://user?id={liked_id}'>{username}</a>")

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
            liked_id=user.telegram_id,
            username=('bu yerga bosing' if not user.username else '@' + user.username)
        )
        if not user.photo_id:
            await message.answer(user_info[:1023])
        else:
            await message.answer_photo(caption=user_info[:1023],
                                       photo=user.photo_id)
        if real_user.premium:
            await send_profile_premium(message, data, bot)

        await asyncio.sleep(3)
    else:
        await send_profile(message, data, bot)

    rand_user = await rand_user_list(message.from_user.id)
    if rand_user is None:
        await message.answer("Uzr hozirchalik sizga mos odam topilmadi,\n"
                             "Adminga yozib ko'ring")
    else:
        await state.update_data(last_profile_user_id=rand_user)
        await create_que(rand_user, message)


@router.message(SearchQues.viewing_ques, F.text == "👎")
async def dislike_que(message: Message, state: FSMContext) -> None:
    user = await rand_user_list(message.from_user.id)
    if user is None:
        await message.answer("Uzr hozirchalik sizga mos odam topilmadi,\n"
                             "Adminga yozib ko'ring")
    else:
        await state.update_data(last_profile_user_id=user)
        await create_que(user, message)


@router.message(SearchQues.viewing_ques, F.text == "shikoyat")
async def complaint_que(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    data = data.get('last_profile_user_id')
    if data:
        await db_commands.create_complaint(message.from_user.id, data)

    user = await rand_user_list(message.from_user.id)
    if user is None:
        await message.answer("Uzr hozirchalik sizga mos odam topilmadi,\n"
                             "Adminga yozib ko'ring")
    else:
        await state.update_data(last_profile_user_id=user)
        await create_que(user, message)


@router.message(SearchQues.viewing_ques, F.text == "🔙")
async def go_back(message: Message, state: FSMContext) -> None:
    await state.set_state(SearchQues.profile_options)
    await profile_choices(message)


@router.callback_query(F.data.startswith("like_"))
async def profile_liked(call: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    await update_user_data(telegram_id=call.message.from_user.id,
                           username=call.message.from_user.username)

    [_, liked_id, liker_id] = call.data.split('_')

    user = await db_commands.select_user(liker_id)

    user_info_template = ("👀Kimdir sizni e'lonizga qiziqdi:\n\n"
                          "{sex_emoji}{name}, {age}, {location}, \n\n" \
                          "📊{height} sm - {weight} kg\n\n" \
                          "🇺🇳Millati: {ethnicity}\n\n" \
                          "👨‍👩‍👧‍👦Oilaviy holati: {marital_status}\n\n" \
                          "{edu_emoji}Ma'lumoti: {education}\n\n" \
                          "💵Kasbi: {occupation}\n\n" \
                          "💢O'zi haqida: {biography}\n\n" \
                          "🔗Akkaunt uchun <a href='tg://user?id={liker_id}'>{username}</a>")
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
        liker_id=liker_id,
        username=('bu yerga bosing' if not user.username else '@' + user.username),
        number="+" + str(user.phone_number)
    )

    await call.message.edit_caption(caption=user_info[:1023], reply_markup=None)
    await start_texting(call, liker_id, liked_id, bot)


@router.callback_query(F.data == "dislike")
async def profile_disliked(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.delete()
    await state.set_state(SearchQues.profile_options)
    await profile_choices(call)
