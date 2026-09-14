"""Модуль для формирования списка частот встречающихся имён"""

import re
from collections import Counter

_NAME_PATTERN = re.compile(
    r"Имя:\s*(?P<name>[А-ЯЁ][^\n]+)"
)


def frequency(text: str) -> Counter:
    """
    По паттерну находит имена в данных анкетируемых.
    Из имён и частот их вхождений формирует словарь.

    :param text: данные анкетируемых, считанные из файла.
    :return counts: отсортированный список кортежей (имя, количество).
    """
    names = (match.group("name").strip() for match in _NAME_PATTERN.finditer(text))

    counts = Counter(names)
    return counts
