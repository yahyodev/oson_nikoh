from asgiref.sync import (
    sync_to_async,
)
from django.db.models import (
    F,
    Q,
)

from django.db.models.expressions import (
    CombinedExpression,
    Value,
)

from tgbot.models import (
    User,
    ViewedProfile
)


@sync_to_async
def check_user_exists(telegram_id: int):
    user_exists = User.objects.filter(telegram_id=telegram_id).exists()
    return user_exists


@sync_to_async
def update_user_data(telegram_id, **kwargs):
    return User.objects.filter(telegram_id=telegram_id).update(**kwargs)


@sync_to_async
def select_user(telegram_id: int):
    try:
        user = User.objects.get(telegram_id=telegram_id)
    except Exception as ex:
        user = User.objects.filter(telegram_id=telegram_id).values().first()
        print(f"Error in select_user {ex}")
    return user


@sync_to_async
def add_user(telegram_id, full_name, username):
    return User(telegram_id=int(telegram_id), full_name=full_name, username=username).save()


@sync_to_async
def search_users(
        need_sex,
        need_age_min,
        need_age_max,
        need_location,
        age,
        offset: int,
        limit: int,
):
    query = (
            Q(is_banned=False)
            & Q(sex=need_partner_sex)
            & (
                    (Q(age__gte=need_age_min) & Q(age__lte=need_age_max))
                    | (Q(age__gte=need_age_min + 1) & Q(age__lte=need_age_max + 1))
            )
            & Q(city=user_need_city)
            & Q(status=True)
    )
    users = User.objects.filter(query).values()
    return users
