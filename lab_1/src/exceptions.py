"""Собственные исключения программы."""


class ProfileError(Exception):
    """Базовый класс для ошибок, связанных с анкетой."""


class ProfileParseError(ProfileError):
    """Анкету не удалось разобрать (например, нет обязательных полей)."""


class ProfileValidationError(ProfileError):
    """Значение одного из полей анкеты не соответствует формату."""


class FileReadError(Exception):
    """Файл не удалось прочитать."""
