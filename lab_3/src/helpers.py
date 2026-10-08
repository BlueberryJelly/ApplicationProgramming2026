"""Классы для хранения цвета. Класс для хранения отступов."""


class Color:
    """Класс хранит данные о цвете в формате BGR."""

    def __init__(self, blue: int, green: int, red: int):
        """Инициализировать поля класса.

        :param blue: синий цвет
        :param green: зелёный цвет
        :param red: красный цвет
        :raises ValueError: значение цвета вне диапазона 0–255
        """
        if any((blue < 0, green < 0, red < 0,
                blue > 255, green > 255, red > 255)):
            raise ValueError("Значение цвета должно быть в диапазоне от 0 до 255 включительно.")
        self.blue = blue
        self.green = green
        self.red = red


class Frame:
    """Класс хранит отступы."""

    def __init__(self, top: int, bottom: int,
                 left: int, right: int):
        """Инициализировать поля класса.

        :param top: отступ сверху
        :param bottom: отступ снизу
        :param left: отступ слева
        :param right: отступ справа
        """
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
