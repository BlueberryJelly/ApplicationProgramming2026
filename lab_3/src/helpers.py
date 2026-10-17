"""Модуль содержит классы для хранения цвета и отступов."""

from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Color:
    """Класс хранит данные о цвете в формате BGR.
    
    Поддерживает сравнение (лексикографическое: сначала blue, затем green, затем red).
    """

    blue: int
    green: int
    red: int

    def __post_init__(self):
        """Проверить валидность значений после инициализации.
        
        :raises ValueError: значение цвета вне диапазона 0–255
        """
        if not (0 <= self.blue <= 255 and 0 <= self.green <= 255 and 0 <= self.red <= 255):
            raise ValueError(
                "Значение цвета должно быть в диапазоне от 0 до 255 включительно."
            )

    @property
    def value(self) -> tuple[int, int, int]:
        """Вернуть значение цвета в виде набора BGR.

        :return: кортеж из трёх цветовых каналов BGR
        """
        return (self.blue, self.green, self.red)


@dataclass
class Frame:
    """Класс хранит отступы в виде чисел-долей изображения от 0 до 1."""

    top: float
    bottom: float
    left: float
    right: float
