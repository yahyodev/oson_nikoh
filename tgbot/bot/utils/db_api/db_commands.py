from typing import List, Union

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
    ViewedProfile,
    Complaint,
    Like, NecessaryLink, Referral
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
        telegram_id: int,
        sex: str,
        age: int = None,
        location: str = None,
        need_age_min: int = None,
        need_age_max: int = None,
        offset: int = None,
        limit: int = None,
) -> List[int]:
    query = (
        Q(status=True)
    )
    if location:
        query &= Q(location=location)
    age_query = Q(active=True)

    if age:
        age_query &= Q(age__gte=(age - 1 if sex == 'ayol' else age - 6))
        age_query &= Q(age__lte=(age + 6 if sex == 'ayol' else age + 1))

    if need_age_min and need_age_max:
        age_query |= Q(age__gte=need_age_min - 2) & Q(age__lte=need_age_max + 2)
    elif need_age_min:
        age_query |= Q(age__gte=need_age_min - 2)
    elif need_age_max:
        age_query |= Q(age__lte=need_age_max + 2)
    query = query & age_query
    users = (User.objects
             .exclude(sex=sex)
             .exclude(telegram_id=telegram_id)
             .filter(query)
             .values_list('telegram_id', flat=True))

    return list(users)


@sync_to_async
def get_user_profiles(user: User):
    users = ViewedProfile.objects.filter(viewer__id=user.id)
    return list(users.values_list('profile__telegram_id', flat=True))


@sync_to_async
def create_complaint(complainer_id: int, accused_id: int) -> None:
    complainer = User.objects.get(telegram_id=complainer_id)
    accused = User.objects.get(telegram_id=accused_id)
    Complaint.objects.get_or_create(complainer=complainer, accused=accused)


@sync_to_async
def create_like(viewer_id: int, profile_id: int) -> None:
    viewer = User.objects.get(telegram_id=viewer_id)
    profile = User.objects.get(telegram_id=profile_id)
    Like.objects.get_or_create(viewer=viewer, profile=profile)


@sync_to_async
def get_like(profile_id: int) -> int:
    likes = Like.objects.filter(profile_id=profile_id)
    if likes:
        return likes.first().viewer
    return 0


@sync_to_async
def select_all_links() -> list:
    links = NecessaryLink.objects.all().values()
    return list(links)

@sync_to_async
def referral_add(link: str, telegram_id: int) -> None:
    Referral.objects.get_or_create(link=link)
    referral = Referral.objects.get(link=link)
    user = User.objects.get(telegram_id=telegram_id)
    user.referral = referral
    user.save()
