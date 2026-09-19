"""Чтение файла с анкетами."""

from src.exceptions import FileReadError


def read_file(filename: str) -> str:
    """Прочитать текстовый файл целиком.

    :param filename: путь к файлу.
    :return: содержимое файла.
    :raises FileReadError: если файл не найден, недоступен
        или имеет неподходящую кодировку.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError as error:
        raise FileReadError(f"Файл '{filename}' не найден") from error
    except IsADirectoryError as error:
        raise FileReadError(f"'{filename}' - это папка, а не файл") from error
    except PermissionError as error:
        raise FileReadError(f"Нет доступа к файлу '{filename}'") from error
    except UnicodeDecodeError as error:
        raise FileReadError(
            f"Файл '{filename}' не в кодировке UTF-8"
        ) from error
    except OSError as error:
        raise FileReadError(
            f"Не удалось прочитать файл '{filename}': {error}"
        ) from error