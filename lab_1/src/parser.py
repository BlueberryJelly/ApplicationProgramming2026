"""Разбор текста файла на отдельные анкеты."""

from src.exceptions import FormParseError
from src.models import Form
from src.patterns import BLOCK_SEPARATOR_RE, FIELD_RE

LABELS: dict[str, str] = {
    "Фамилия": "surname",
    "Имя": "name",
    "Пол": "gender",
    "Дата рождения": "birth_date",
    "Номер телефона или email": "contact",
    "Город": "city",
}


def split_blocks(text: str) -> list[str]:
    """Разделить текст на блоки анкет (анкеты разделены пустой строкой).

    :param text: содержимое файла.
    :return: список непустых блоков.
    """
    blocks = BLOCK_SEPARATOR_RE.split(text)
    return [block for block in blocks if block.strip()]


def parse_block(block: str) -> Form:
    """Преобразовать блок текста в анкету.

    :param block: текст одной анкеты.
    :return: объект Form.
    :raises FormParseError: если в блоке нет обязательных полей.
    """
    fields: dict[str, str] = {}
    for label, value in FIELD_RE.findall(block):
        key = LABELS.get(label.strip())
        if key is not None:
            fields[key] = value.strip()

    missing = [label for label, key in LABELS.items() if key not in fields]
    if missing:
        raise FormParseError(
            "Не найдены поля: " + ", ".join(missing)
        )
    return Form(**fields)
