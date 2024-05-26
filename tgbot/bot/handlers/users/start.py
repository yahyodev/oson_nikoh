from aiogram import Router, types
from aiogram.filters import CommandStart, CommandObject
from aiogram.client.session.middlewares.request_logging import logger
from aiogram.fsm.context import FSMContext

from tgbot.bot.loader import bot
from django.conf import settings

from tgbot.models import User
from tgbot.bot.utils.db_api import db_commands
from tgbot.bot.states import RegData
from tgbot.bot.keyboards.inline import start_keyboard
from tgbot.bot.functions.common import update_user_data

router = Router()


@router.message(CommandStart())
async def register_user(message: types.Message,
                        command: CommandObject,
                        state: FSMContext) -> None:
    username = message.from_user.username if message.from_user.username else ""
    telegram_id = message.from_user.id
    full_name = message.from_user.full_name
    user_exists = await db_commands.check_user_exists(telegram_id)
    markup = await start_keyboard(message)
    text = "👋Assalomu aleykum, {full_name}\n\n" \
           "💍Oson Nikoh botiga xush kelibsiz!\n\n" \
           "👰Bu yerda jufti halolizni topsangiz bo'ladi\n\n" \
           "❓Barcha savollar @oson_nikoh_admin'ga" \
        .format(full_name=message.from_user.full_name)
    status = False
    if not user_exists:
        await db_commands.add_user(telegram_id=message.from_user.id,
                                   full_name=message.from_user.full_name,
                                   username=message.from_user.username,
                                   )
        args = command.args
        if args:
            await db_commands.referral_add(link=f"{args}",
                                           telegram_id=message.from_user.id)
            ref_link = int(args)
            users = await db_commands.get_all_users()
            count = await db_commands.filter_referral(args)
            print(ref_link, users, count)
            if ref_link in users:
                if count < 5:
                    await bot.send_message(int(args), f"Sizni ssilkezdan {full_name} {count}chi bo'lib qo'shildi\n" \
                                           "🎁5ta odamga yetganda VIP ya'ni premium olasiz")
                if count >= 5:
                    await bot.send_message(int(args), f"Sizni ssilkezdan {full_name} {count}chi bo'lib qo'shildi\n" \
                                           "💵Siz VIP tarifiga qo'shildiz, endi xohlagan odamizni akkauntini srazu olasiz")
                    await update_user_data(int(args), premium=True)
    else:
        status = status or (await db_commands.select_user(message.from_user.id)).status
        await update_user_data(telegram_id=telegram_id,
                               full_name=message.from_user.full_name,
                               username=message.from_user.username,
                               is_fake=False)
    if not status:
        await state.set_state(RegData.start)
    else:
        await state.clear()

    await message.answer(text, reply_markup=markup)
