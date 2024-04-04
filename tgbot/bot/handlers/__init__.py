from aiogram import Router

from tgbot.bot.filters import IsPrivate


def setup_routers() -> Router:
    from .users import start, help, echo, registration, my_profile
    from .errors import error_handler

    router = Router()

    # Agar kerak bo'lsa, o'z filteringizni o'rnating
    start.router.message.filter(IsPrivate())
    registration.router.message.filter(IsPrivate())
    # TODO srazu register bo'lib ketish kere nima tugmani bossayam
    router.include_routers(start.router, help.router, registration.router, my_profile.router, echo.router,
                           error_handler.router)

    return router
