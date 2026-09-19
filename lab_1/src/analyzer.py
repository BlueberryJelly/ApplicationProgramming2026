"""Подсчёт имён в валидных анкетах."""

from collections import Counter

from src.exceptions import FormError
from src.parser import parse_block, split_blocks
from src.validators import validate_form


class NameCounter:
    """Счётчик имён."""

    def __init__(self) -> None:
        """Создать пустой счётчик."""
        self._counter: Counter[str] = Counter()

    def add(self, name: str) -> None:
        """Учесть одно вхождение имени."""
        self._counter[name] += 1

    def most_common(self) -> list[tuple[str, int]]:
        """Вернуть самые частые имена.

        :return: список пар (имя, количество). Если несколько имён
            делят максимум, возвращаются все. Пустой список, если
            имён нет.
        """
        if not self._counter:
            return []
        max_count = max(self._counter.values())
        return [
            (name, count)
            for name, count in self._counter.items()
            if count == max_count
        ]


def count_names(text: str) -> NameCounter:
    """Посчитать имена во всех валидных анкетах.

    Анкеты, которые не удалось разобрать или которые не прошли
    проверку, пропускаются.

    :param text: содержимое файла.
    :return: заполненный счётчик имён.
    """
    counter = NameCounter()
    for block in split_blocks(text):
        try:
            form = parse_block(block)
            validate_form(form)
        except FormError:
            continue
        counter.add(form.name)
    return counter
