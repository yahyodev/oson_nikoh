from __future__ import annotations

from typing import Union

from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.client.session.middlewares.request_logging import logger
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram import F

from django.conf import settings

from tgbot.bot.functions.auxiliary_tools import display_profile, profile_choices
from tgbot.bot.utils.db_api import db_commands
from tgbot.bot.utils.datas import regions
from tgbot.bot.functions.common import update_user_data

from tgbot.bot.states import RegData, SearchQues
from tgbot.bot.keyboards.reply import request_contact
from tgbot.bot.keyboards.builders import form_btn
from tgbot.bot.keyboards.builders import get_regions

from tgbot.bot.loader import logger

router = Router()


@router.message(RegData.start)
@router.callback_query(RegData.start)
async def registration(obj: CallbackQuery | Message, state: FSMContext) -> None:
    message = obj.message if isinstance(obj, CallbackQuery) else obj
    user = await db_commands.select_user(message.from_user.id)
    if not user or (user and not user.status):
        contact_keyboard = await request_contact()
        await state.set_state(RegData.contact)
        await message.answer("Boshlash uchun telefon nomeringiz kerak,\n"
                             "Pastdagi tugmani bosing",
                             reply_markup=contact_keyboard)
        await state.set_state(RegData.contact)
        # await message.answer("Ismingizni ayting",
        #                      reply_markup=form_btn(obj.from_user.first_name))
    else:
        ...
        await message.edit_text(
            reply_markup=...,
            text="Siz allaqachon ro'xatdan o'tgansiz,\n"
                 "xohlasangiz anketangizni o'zgartirishingiz mumkin,\n"
                 "o'zgaritirsh uchun pastdagi tugmani bosing"
        )


@router.message(RegData.contact, F.contact.user_id == F.from_user.id)
async def contact(message: Message, state: FSMContext) -> None:
    await update_user_data(telegram_id=message.from_user.id,
                           phone_number=message.contact.phone_number,
                           )
    await state.set_state(RegData.name)
    await message.answer("Ismingizni ayting",
                         reply_markup=form_btn(message.from_user.first_name))


@router.message(RegData.contact)
async def contact(message: Message, state: FSMContext) -> None:
    markup = await request_contact()
    await message.answer("Tugmani bosing", reply_markup=markup)


@router.message(RegData.name, F.text)
async def name(message: Message, state: FSMContext) -> None:
    await update_user_data(telegram_id=message.from_user.id,
                           name=message.text)
    await state.set_state(RegData.age)
    await message.answer("Yoshingizni yozing")


@router.message(RegData.age, F.text.isdigit())
async def age(message: Message, state: FSMContext) -> None:
    if int(message.text) < 18:
        await message.answer("Ro'yxatdan o'tishga yoshingiz kichik")
    elif int(message.text) > 99:
        await message.answer("Tu'gilgan yilingizni emas, yoshingizni kiriting\n"
                             "Masalan, 35")
    else:
        await update_user_data(telegram_id=message.from_user.id,
                               age=int(message.text))
        await state.set_state(RegData.sex)
        await message.answer(
            "Jinsingizni tanlang",
            reply_markup=form_btn(["erkak", "ayol"])
        )


@router.message(RegData.age, ~F.text.isdigit())
async def age(message: Message, state: FSMContext) -> None:
    await message.answer("Faqat raqamlar kiriting,\n"
                         "Masalan, 32")


@router.message(RegData.sex, F.text.in_(["erkak", "ayol"]))
async def sex(message: Message, state: FSMContext) -> None:
    await update_user_data(telegram_id=message.from_user.id,
                           sex=message.text)
    await state.set_state(RegData.location)
    await message.answer("Viloyatingizni tanlang",
                         reply_markup=get_regions())


@router.message(RegData.sex, ~F.text.in_(["erkak", "ayol"]))
async def sex(message: Message, state: FSMContext) -> None:
    await message.answer("Bir tugmani tanlang",
                         reply_markup=form_btn(["erkak", "ayol"]))


@router.message(RegData.location, F.text.in_(regions.keys()))
async def location(message: Message, state: FSMContext) -> None:
    await update_user_data(telegram_id=message.from_user.id,
                           location=message.text)
    await state.set_state(RegData.height)
    await message.answer("Bo'yingizni yozing smda(masalan, 165)")


@router.message(RegData.location, ~F.text.in_(regions.keys()))
async def location(message: Message, state: FSMContext) -> None:
    await message.answer("Iltimos biror viloyatni tanlang", reply_markup=get_regions())


@router.message(RegData.height, F.text.isdigit())
async def height(message: Message, state: FSMContext) -> None:
    await update_user_data(telegram_id=message.from_user.id,
                           height=int(message.text))
    await state.set_state(RegData.weight)
    await message.answer("Vazningizni yozing kgda(masalan, 60)")


@router.message(RegData.height, ~F.text.isdigit())
async def height(message: Message) -> None:
    await message.answer("Iltimos faqat raqamlar ishlating")


@router.message(RegData.weight, F.text.isdigit())
async def weight(message: Message, state: FSMContext) -> None:
    await update_user_data(telegram_id=message.from_user.id,
                           weight=int(message.text))
    await state.set_state(RegData.ethnicity)
    await message.answer("Millatingizni yozing")


@router.message(RegData.weight, ~F.text.isdigit())
async def weight(message: Message) -> None:
    await message.answer("Iltimos faqat raqamlar ishlating")


@router.message(RegData.ethnicity, F.text)
async def ethnicity(message: Message, state: FSMContext) -> None:
    await update_user_data(telegram_id=message.from_user.id,
                           ethnicity=message.text)
    await state.set_state(RegData.marital_status)
    await message.answer("Oilaviy holatingizni yozing(masalan, ajrashgan)")


@router.message(RegData.marital_status, F.text)
async def marital_status(message: Message, state: FSMContext) -> None:
    await update_user_data(telegram_id=message.from_user.id,
                           marital_status=message.text)
    await state.set_state(RegData.education)
    await message.answer("Ma'lumotingizni yozing(masalan, oliy)")


@router.message(RegData.education, F.text)
async def education(message: Message, state: FSMContext) -> None:
    await update_user_data(telegram_id=message.from_user.id,
                           education=message.text)
    await state.set_state(RegData.occupation)
    await message.answer("Kasbingizni yozing(masalan, o'qituvchi)")


@router.message(RegData.occupation, F.text)
async def occupation(message: Message, state: FSMContext) -> None:
    await update_user_data(telegram_id=message.from_user.id,
                           occupation=message.text)
    await state.set_state(RegData.biography)
    await message.answer("O'zingiz va talablaringiz haqida yozing")


@router.message(RegData.biography, F.text)
async def biography(message: Message, state: FSMContext) -> None:
    await update_user_data(telegram_id=message.from_user.id,
                           biography=message.text)

    user = await db_commands.select_user(message.from_user.id)
    if user:
        partner = 'kuyov' if user.sex == 'ayol' else 'kelin'
    else:
        partner = 'jufti halolingiz'
    await message.answer(f"{partner.capitalize()} uchun eng kichik yoshni ayting(masalan, 18)")

    await state.set_state(RegData.min_age)


@router.message(RegData.min_age, F.text.isdigit())
async def min_age(message: Message, state: FSMContext) -> None:
    if int(message.text) < 18:
        await message.answer("Bu qonunga xilof, kattaroq yosh kiriting")
    elif int(message.text) > 99:
        await message.answer("Tu'gilgan yilini emas, yoshini kiriting\n"
                             "Masalan, 18")
    else:
        await update_user_data(telegram_id=message.from_user.id,
                               need_partner_age_min=int(message.text))

        user = await db_commands.select_user(message.from_user.id)
        if user:
            partner = 'kuyov' if user.sex == 'ayol' else 'kelin'
        else:
            partner = 'jufti halolingiz'
        await message.answer(f"{partner.capitalize()} uchun eng katta yoshni ayting(masalan, 58)")

        await state.set_state(RegData.max_age)


@router.message(RegData.min_age, ~F.text.isdigit())
async def min_age(message: Message, state: FSMContext) -> None:
    await message.answer("Faqat raqamlar kiriting,\n"
                         "Masalan, 18")


@router.message(RegData.max_age, F.text.isdigit())
async def max_age(message: Message, state: FSMContext) -> None:
    if int(message.text) < 18:
        await message.answer("Bu qonunga xilof, kattaroq yosh kiriting")
    elif int(message.text) > 99:
        await message.answer("Tu'gilgan yilini emas, yoshini kiriting\n"
                             "Masalan, 58")
    else:
        await update_user_data(telegram_id=message.from_user.id,
                               need_partner_age_max=int(message.text))
        await state.set_state(RegData.photo)
        await message.answer("Endi foto yuboring, birovnikini qo'ymang,\n"
                             "buni boshqa foydalanuvchilar ko'ra oladi")


@router.message(RegData.max_age, ~F.text.isdigit())
async def max_age(message: Message, state: FSMContext) -> None:
    await message.answer("Faqat raqamlar kiriting,\n"
                         "Masalan, 58")


@router.message(RegData.photo, F.photo)
async def photo(message: Message, state: FSMContext) -> None:
    photo_file_id = message.photo[-1].file_id
    await update_user_data(telegram_id=message.from_user.id,
                           photo_id=photo_file_id)
    await state.clear()
    await update_user_data(telegram_id=message.from_user.id, status=True)
    await display_profile(message)
    await profile_choices(message)
    await state.set_state(SearchQues.profile_options)


@router.message(RegData.photo, ~F.photo)
async def photo(message: Message) -> None:
    await message.answer("Foto yuborilishi shart, qayta urinib ko'ring")
