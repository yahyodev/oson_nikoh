from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from tgbot.bot.functions.auxiliary_tools import profile_choices
from tgbot.bot.keyboards.inline import start_keyboard
from tgbot.bot.loader import dp
from tgbot.bot.states import SearchQues, RegData
from tgbot.bot.utils.db_api import db_commands

router = Router()


@router.message()
async def echo(message: types.Message, state: FSMContext):
    # await message.answer(message.text)
    user_exists = await db_commands.check_user_exists(message.from_user.id)
    if not user_exists:
        await db_commands.add_user(telegram_id=message.from_user.id,
                                   full_name=message.from_user.full_name,
                                   username=message.from_user.username,
                                   )

    user = await db_commands.select_user(message.from_user.id)
    if user and user.status:
        await state.set_state(SearchQues.profile_options)
        await message.answer("Qayta urinib ko'ring...")
        await profile_choices(message)
    else:
        markup = await start_keyboard(message)
        text = "👋Assalomu aleykum, {full_name}\n\n" \
               "💍Oson Nikoh botiga xush kelibsiz!\n\n" \
               "👰Bu yerda jufti halolizni topsangiz bo'ladi\n\n" \
               "❓Barcha savollar @oson_nikoh_admin'ga" \
            .format(full_name=message.from_user.full_name)
        await state.set_state(RegData.start)
        await message.answer(text, reply_markup=markup)
