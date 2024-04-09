from aiogram.fsm.state import (StatesGroup,
                               State)


class RegData(StatesGroup):
    start = State()
    contact = State()
    name = State()
    age = State()
    sex = State()
    location = State()
    height = State()
    weight = State()
    ethnicity = State()
    marital_status = State()
    education = State()
    occupation = State()
    biography = State()
    min_age = State()
    max_age = State()
    photo = State()


class ChangeData(StatesGroup):
    start = State()
    biography = State()
    photo = State()


class SearchQues(StatesGroup):
    profile_options = State()
    viewing_ques = State()


class Filters(StatesGroup):
    using = State()
    min = State()
    max = State()

