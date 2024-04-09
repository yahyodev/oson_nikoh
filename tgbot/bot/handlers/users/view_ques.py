import asyncio
from typing import Union

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from tgbot.bot.functions.auxiliary_tools import profile_choices, send_profile, start_texting
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
    await update_user_data(obj.from_user.id, username=obj.from_user.username)
    await state.set_state(SearchQues.viewing_ques)
    await update_user_data(obj.from_user.id, active=True)
    user = await rand_user_list(obj.from_user.id)
    await state.update_data(last_profile_user_id=user)
    await create_que(user, obj)


@router.message(SearchQues.viewing_ques, F.text == "👍")
async def like_que(message: Message, state: FSMContext, bot: Bot) -> None:
    data = await state.get_data()
    data = data.get('last_profile_user_id')
    await send_profile(message, data, bot)

    user = await rand_user_list(message.from_user.id)
    await state.update_data(last_profile_user_id=user)
    await create_que(user, message)


@router.message(SearchQues.viewing_ques, F.text == "👎")
async def dislike_que(message: Message, state: FSMContext) -> None:
    user = await rand_user_list(message.from_user.id)
    await state.update_data(last_profile_user_id=user)
    await create_que(user, message)


@router.message(SearchQues.viewing_ques, F.text == "shikoyat")
async def complaint_que(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    data = data.get('last_profile_user_id')
    if data:
        await db_commands.create_complaint(message.from_user.id, data)

    user = await rand_user_list(message.from_user.id)
    await state.update_data(last_profile_user_id=user)
    await create_que(user, message)


@router.message(SearchQues.viewing_ques, F.text == "🔙")
async def go_back(message: Message, state: FSMContext) -> None:
    await state.set_state(SearchQues.profile_options)
    await profile_choices(message)


@router.callback_query(F.data.startswith("like_"))
async def profile_liked(call: CallbackQuery, state: FSMContext, bot: Bot) -> None:
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
        username=('bu yerga bosing' if not user.username else '@' + user.username)
    )

    await call.message.edit_caption(caption=user_info, reply_markup=None)
    await start_texting(call, liker_id, liked_id, bot)


@router.callback_query(F.data == "dislike")
async def profile_disliked(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.delete()
    await state.set_state(SearchQues.profile_options)
    await profile_choices(call)