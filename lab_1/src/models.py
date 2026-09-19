"""Модель данных анкеты."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Form:
    """Анкета человека (значения полей хранятся как строки)."""

    surname: str
    name: str
    gender: str
    birth_date: str
    contact: str
    city: str