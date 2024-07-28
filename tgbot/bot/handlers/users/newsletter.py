import asyncio

from aiogram import Router, types, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.client.session.middlewares.request_logging import logger
from aiogram.fsm.context import FSMContext
from environs import Env

from tgbot.bot.loader import bot
from django.conf import settings

from tgbot.models import User
from tgbot.bot.utils.db_api import db_commands
from tgbot.bot.states import RegData
from tgbot.bot.keyboards.inline import start_keyboard
from tgbot.bot.functions.common import update_user_data

router = Router()


@router.message(F.text.startswith('/newsletter'))
async def newsletter(message: types.Message):
    print('hiii')
    env = Env()
    env.read_env()
    ADMINS = list(env.list("ADMINS"))

    if f"{message.from_user.id}" in ADMINS:
        msg = message.text[12:]
        users = await db_commands.get_all_users()
        for user in users:
            try:
                await bot.send_message(user, msg)
                await bot.send_message(message.from_user.id, f"Successful newsletter {user}")
            except:
                await update_user_data(active=False)
                await bot.send_message(message.from_user.id, f"Unsuccessful newsletter {user}")

            await asyncio.sleep(0.1)
