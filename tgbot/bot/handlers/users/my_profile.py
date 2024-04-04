from typing import Union

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, Message
from aiogram.filters import Command

from tgbot.bot.states import ChangeData, RegData
from tgbot.bot.functions.auxiliary_tools import display_profile, profile_choices
from tgbot.bot.keyboards.builders import form_btn
from tgbot.bot.utils.db_api.db_commands import update_user_data

router = Router()


# @router.callback_query(F.data == "my_profile")
# async def my_profile(call: CallbackQuery):
#     await profile_choices(call)


@router.message(F.text == '2', ChangeData.start)
async def change_que_completely(message: Message, state: FSMContext):
    await message.answer("Boshlash uchun ismingizni ayting",
                         reply_markup=form_btn(message.from_user.first_name))
    await state.set_state(RegData.name)


@router.message(F.text == '3', ChangeData.start)
async def change_bio(message: Message, state: FSMContext):
    await state.set_state(ChangeData.biography)
    await message.answer("O'zingiz haqida bo'lgan boshqa ma'lumotlarni ayting\n"
                         "xohlasangiz talablaringizni ham yozing")


@router.message(ChangeData.biography, F.text)
async def biography(message: Message, state: FSMContext) -> None:
    await state.clear()
    await update_user_data(telegram_id=message.from_user.id,
                           biography=message.text)


@router.message(F.text == '4', ChangeData.start)
async def change_photo(message: Message, state: FSMContext):
    await state.set_state(ChangeData.photo)
    await message.answer("Foto yuboring, birovnikini qo'ymang,\n"
                         "buni boshqa foydalanuvchilar ko'ra oladi")


@router.message(ChangeData.photo, F.photo)
async def photo(message: Message, state: FSMContext) -> None:
    photo_file_id = message.photo[-1].file_id
    await update_user_data(telegram_id=message.from_user.id,
                           photo_id=photo_file_id)
    await state.clear()


@router.message(ChangeData.photo, ~F.photo)
async def photo(message: Message) -> None:
    await message.answer("Foto yuborilishi shart, qayta urinib ko'ring")


# to fix states

@router.message(F.text == '1')
async def view_ques(message: Message):
    await update_user_data(telegram_id=message.from_user.id,
                           active=True)


@router.message(F.text == '2')
@router.message(Command('my_profile'))
@router.callback_query(F.data == 'my_profile')
async def my_profile(obj: Union[Message, CallbackQuery], state: FSMContext):
    if isinstance(obj, CallbackQuery):
        obj = obj.message

    await display_profile(obj)

    text = "1. Anketalarni ko'rish\n" \
           "2. Anketamni qayta boshidan to'ldirib chiqish\n" \
           "3. O'zim haqidagi ma'lumotni o'zgartirish\n" \
           "4. Fotoni o'zgartirish"

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
    await state.set_state(ChangeData.start)
    await (obj
           .answer(text, reply_markup=keyboard))


@router.message(F.text == '3')
async def deactivate_que(message: Message, state: FSMContext):
    await state.clear()
    await update_user_data(telegram_id=message.from_user.id,
                           active=False)
    await message.answer("Sizning anketangiz olib tashlandi,\n"
                         "Baxtingizni topdingiz degan umiddamiz!\n\n\n"
                         "Anketalarni ko'rishga tugmani bosing",
                         reply_markup=form_btn("Anketalarni ko'rish"))
