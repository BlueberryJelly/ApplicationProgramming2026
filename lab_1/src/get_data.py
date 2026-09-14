"""Модуль для записи данных из файла в переменную."""

import argparse
import pathlib


def get_data() -> str:
    """
    Получает путь к файлу из аргументов командной строки.
    Записывает данные из файла в переменную.

    :return text: данные, считанные из файла.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-path", type=pathlib.Path,
                        required=True, help="Путь к файлу с данными")
    args = parser.parse_args()

    if not args.data_path.exists():
        raise SystemExit(f"Входные данные не найдены: файл {args.data_path} не существует.")

    if not args.data_path.is_file():
        raise SystemExit(f"Указанный путь не является файлом: {args.data_path}")

    with args.data_path.open(mode="r", encoding="utf-8") as file:
        text = file.read()
    return text
