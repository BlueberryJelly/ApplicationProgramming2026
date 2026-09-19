"""Проверка значений полей анкеты."""

from datetime import date

from src.exceptions import FormValidationError
from src.models import Form
from src.patterns import (
    CITY_RE,
    DATE_RE,
    EMAIL_RE,
    GENDER_RE,
    NAME_RE,
    PHONE_RE,
)


def is_valid_name(value: str) -> bool:
    """Проверить фамилию или имя (начинается с заглавной буквы)."""
    return NAME_RE.fullmatch(value) is not None


def is_valid_gender(value: str) -> bool:
    """Проверить поле «Пол»."""
    return GENDER_RE.fullmatch(value) is not None


def is_valid_date(value: str) -> bool:
    """Проверить дату рождения.

    Формат проверяется регулярным выражением, затем проверяется, что
    такая дата существует (например, нет 31.02).

    :param value: строка с датой.
    :return: True, если дата корректна.
    """
    match = DATE_RE.fullmatch(value)
    if match is None:
        return False

    day = int(match["day"])
    month = int(match["month"])
    year = int(match["year"])
    try:
        date(year, month, day)
    except ValueError:
        return False
    return True


def is_valid_contact(value: str) -> bool:
    """Проверить номер телефона или email."""
    return (
        PHONE_RE.fullmatch(value) is not None
        or EMAIL_RE.fullmatch(value) is not None
    )


def is_valid_city(value: str) -> bool:
    """Проверить город (формат: Москва или г. Москва)."""
    return CITY_RE.fullmatch(value) is not None


def validate_form(form: Form) -> None:
    """Проверить все поля анкеты.

    :param form: анкета.
    :raises FormValidationError: если какое-либо поле некорректно.
    """
    checks = (
        ("Фамилия", form.surname, is_valid_name),
        ("Имя", form.name, is_valid_name),
        ("Пол", form.gender, is_valid_gender),
        ("Дата рождения", form.birth_date, is_valid_date),
        ("Номер телефона или email", form.contact, is_valid_contact),
        ("Город", form.city, is_valid_city),
    )
    for label, value, check in checks:
        if not check(value):
            raise FormValidationError(
                f"Некорректное поле '{label}': '{value}'"
            )
        