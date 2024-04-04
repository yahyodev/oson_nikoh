from typing import Union

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from tgbot.bot.functions.auxiliary_tools import profile_choices
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
    await state.set_state(SearchQues.viewing_ques)
    await update_user_data(obj.from_user.id, active=True)
    user = await rand_user_list(obj.from_user.id)
    await state.update_data(last_profile_user_id=user)
    await create_que(user, obj)


@router.message(SearchQues.viewing_ques, F.text == "👍")
async def like_que(message: Message, state: FSMContext) -> None:
    user = await rand_user_list(message.from_user.id)
    await state.update_data(last_profile_user_id=user)
    await create_que(user, message)


@router.message(SearchQues.viewing_ques, F.text == "👎")
async def dislike_que(message: Message, state: FSMContext) -> None:
    user = await rand_user_list(message.from_user.id)
    await state.update_data(last_profile_user_id=user)
    await create_que(user, message)


@router.message(SearchQues.viewing_ques, F.text == "🚫")
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
