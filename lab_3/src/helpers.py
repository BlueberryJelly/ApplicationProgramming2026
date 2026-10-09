"""Модуль содержит классы для хранения цвета и отступов."""

from dataclasses import dataclass

class Color:
    """Класс хранит данные о цвете в формате BGR."""

    def __init__(self, blue: int, green: int, red: int):
        """Инициализировать поля класса.

        :param blue: синий цвет
        :param green: зелёный цвет
        :param red: красный цвет
        :raises ValueError: значение цвета вне диапазона 0–255
        """
        if not (0 <= blue <= 255 and 0 <= green <= 255 and 0 <= red <= 255):
            raise ValueError("Значение цвета должно быть в диапазоне от 0 до 255 включительно.")
        self.blue = blue
        self.green = green
        self.red = red

    @property
    def value(self) -> tuple[int, int, int]:
        """Вернуть значение цвета в виде набора BGR.

        :return: кортеж из трёх цветовых каналов BGR
        """
        return [self.blue, self.green, self.red]


@dataclass
class Frame:
    """Класс хранит отступы в виде чисел-долей изображения от 0 до 1."""

    top: float
    bottom: float
    left: float
    right: float
