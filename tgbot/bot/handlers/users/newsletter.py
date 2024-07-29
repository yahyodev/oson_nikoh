import asyncio

from aiogram import Router, types, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
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
from tgbot.bot.states.newsletter_states import CreateMessage

router = Router()


@router.message(F.text.startswith('/newsletter'))
async def newsletter(message: types.Message, state: FSMContext):
    env = Env()
    env.read_env()
    ADMINS = list(env.list("ADMINS"))

    if f"{message.from_user.id}" in ADMINS:
        await message.answer("Siz newsletter xabarini yuboryapsiz")
        await message.answer("Newsletter matnini yuboring")
        await state.set_state(CreateMessage.get_text)
    else:
        await message.answer("Bu operatsiyani o'tkazishga sizni huquqingiz yo'q")



@router.message(F.text, CreateMessage.get_text)
async def set_text_handler(message: Message, state: FSMContext):
    await state.update_data(text=message.md_text)
    await message.answer("Endi foto yuboring")
    await state.set_state(CreateMessage.get_photo)


@router.message(F.photo, CreateMessage.get_photo)
async def set_photo_handler(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    await message.answer("Endi tugma uchun matn yuboring")
    await state.set_state(CreateMessage.get_keyboard_text)


@router.message(F.text, CreateMessage.get_keyboard_text)
async def set_kb_text_handler(message: Message, state: FSMContext):
    await state.update_data(kb_text=message.text)
    await message.answer("Endi tugma uchun havola yuboring")
    await state.set_state(CreateMessage.get_keyboard_url)


@router.message(F.text, CreateMessage.get_keyboard_url)
async def set_kb_url_handler(message: Message, state: FSMContext):
    await state.update_data(kb_url=message.text)
    await state.update_data(admin=message.from_user.id)
    data = await state.get_data()
    btn = InlineKeyboardButton(text=data["kb_text"], url=data["kb_url"])
    confirm_btn = InlineKeyboardButton(text="tasdiqlash", callback_data="confirmed_newsletter")
    markup = InlineKeyboardMarkup(inline_keyboard=[], row_width=1, one_time_keyboard=True)
    markup.inline_keyboard.append([btn, confirm_btn])
    await message.answer_photo(caption=f"Tasdiqlang\n\n"
                                       f"{data['text']}",
                               photo=data['photo'],
                               reply_markup=markup)

@router.callback_query(F.data=="confirmed_newsletter")
async def send(message: Message, state: FSMContext):
    data = await state.get_data()
    await bot.send_message(chat_id=data['admin'], text='Newsletter boshlandi')
    await state.clear()

    btn = InlineKeyboardButton(text=data["kb_text"], url=data["kb_url"])
    markup = InlineKeyboardMarkup(inline_keyboard=[], row_width=1, one_time_keyboard=True)
    markup.inline_keyboard.append([btn])
    # await message.answer_photo(caption= f"{data['text']}",
    #                            photo=data['photo'],
    #                            reply_markup=markup)

    users = await db_commands.get_all_users()
    count = 0
    for user in users:
        try:
            await bot.send_photo(photo=data['photo'],
                                 caption=data['text'],
                                 reply_markup=markup,
                                 chat_id=user)
            count += 1
        except:
            pass
        await asyncio.sleep(0.05)

    await bot.send_message(chat_id=data['admin'],
                           text=f"Shuncha odamga yuborildi {count}")
    # msg = message.text[12:]
    # users = await db_commands.get_all_users()
    # for user in users:
    #     try:
    #         await bot.send_message(user, msg)
    #         await bot.send_message(message.from_user.id, f"Successful newsletter {user}")
    #     except:
    #         await update_user_data(active=False)
    #         await bot.send_message(message.from_user.id, f"Unsuccessful newsletter {user}")
    #
    #     await asyncio.sleep(0.1)