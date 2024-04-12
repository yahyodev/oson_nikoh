from typing import Union

from aiogram import types, BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramAPIError

from tgbot.bot.keyboards.inline.necessary_links import necessary_links_keyboard
from tgbot.bot.utils.db_api import db_commands


class CheckSubscriberMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def __call__(self, handler, obj: Union[Message, CallbackQuery], data=None):
        if isinstance(obj, CallbackQuery):
            obj = obj.message
        user_id = obj.from_user.id
        chat_id = obj.chat.id

        try:
            links_db = await db_commands.select_all_links()
            subscribed_links = set()

            async def check_subscription(link_id):
                check = await obj.bot.get_chat_member(chat_id=link_id, user_id=user_id)
                return check.status != "left"

            for link in links_db:
                if await check_subscription(link["telegram_link_id"]):
                    subscribed_links.add(link["telegram_link_id"])
            text, markup = (
                "Вы подписались не на все каналы! Чтобы продолжить пользоваться ботом, "
                "подпишитесь! Ссылки ниже: "
            ), await necessary_links_keyboard(
                telegram_id=user_id,
                links_db=links_db,
            )

            if len(subscribed_links) < len(links_db):
                await obj.answer(text=text, reply_markup=markup)
                return
        except TelegramAPIError as e:
            # Handle API errors
            print(f"Error checking subscriber status: {e}")
            await obj.answer("Failed to check your subscription status. Please try again later.")
            return await handler(obj, data)
            # fix this

        return await handler(obj, data)
