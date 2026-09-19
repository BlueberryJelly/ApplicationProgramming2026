"""Регулярные выражения для разбора и проверки анкет."""

import re

BLOCK_SEPARATOR_RE: re.Pattern[str] = re.compile(r"\n\s*\n")

FIELD_RE: re.Pattern[str] = re.compile(
    r"^([^:\n]+):[ \t]*(.*)$", re.MULTILINE
)

NAME_RE: re.Pattern[str] = re.compile(r"^[А-ЯЁ][а-яё]+(?:-[А-ЯЁ][а-яё]+)*$")

GENDER_RE: re.Pattern[str] = re.compile(
    r"^(?:Мужской|мужской|Женский|женский|[МмЖж])$"
)

DATE_RE: re.Pattern[str] = re.compile(
    r"(?P<day>0?[1-9]|[12]\d|3[01])"
    r"(?P<sep>[/.-])"
    r"(?P<month>0?[1-9]|1[0-2])"
    r"(?P=sep)"
    r"(?P<year>19\d{2}|20[01]\d|202[0-6])"
)

PHONE_RE: re.Pattern[str] = re.compile(
    r"(?:8|\+7)(?:"
    r"\d{10}"
    r"| \(\d{3}\) \d{3}(?:-\d{2}-\d{2}| \d{2} \d{2})"
    r"| \d{3} \d{3}(?:-\d{2}-\d{2}| \d{2} \d{2})"
    r")"
)

EMAIL_RE: re.Pattern[str] = re.compile(
    r"^[A-Za-z0-9._%+-]{1,64}@(?:gmail\.com|mail\.ru|yandex\.ru)$"
)

CITY_RE: re.Pattern[str] = re.compile(
    r"^(?:г\. )?[А-ЯЁ][а-яё]+(?:[- ][А-ЯЁ][а-яё]+)*$"
)
