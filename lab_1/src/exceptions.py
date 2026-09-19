"""Собственные исключения программы."""


class FormError(Exception):
    """Базовый класс для ошибок, связанных с анкетой."""


class FormParseError(FormError):
    """Анкету не удалось разобрать (например, нет обязательных полей)."""


class FormValidationError(FormError):
    """Значение одного из полей анкеты не соответствует формату."""


class FileReadError(Exception):
    """Файл не удалось прочитать."""
