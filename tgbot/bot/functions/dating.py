from typing import (
    List,
)

from tgbot.bot.utils.db_api import (
    db_commands,
)


async def get_next_user(
        telegram_id: int
) -> List[int]:
    user = await db_commands.select_user(telegram_id)
    viewed_profiles = user.viewed_profiles.all()

    viewed_profiles_ids = [profile.telegram_id for profile in viewed_profiles]
    need_sex = 'ayol' if user.sex == 'erkak' else 'erkak'
    user_filter = await db_commands.search_users(

    )

    user_list = []
