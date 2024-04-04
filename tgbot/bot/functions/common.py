from tgbot.bot.utils.db_api import db_commands
from asyncpg import UniqueViolationError


async def update_user_data(telegram_id: int, **kwargs) -> None:
    try:
        await db_commands.update_user_data(telegram_id=telegram_id, **kwargs)
    except UniqueViolationError:
        pass
