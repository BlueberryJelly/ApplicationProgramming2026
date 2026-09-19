"""Поиск самого частого имени среди валидных анкет.

Запуск: python main.py data.txt
"""

import argparse
import sys

from src.analyzer import count_names
from src.exceptions import FileReadError
from src.file_reader import read_file


def parse_args() -> argparse.Namespace:
    """Разобрать аргументы командной строки.

    :return: пространство имён с атрибутом filename.
    """
    parser = argparse.ArgumentParser(
        description="Найти самое частое имя среди валидных анкет."
    )
    parser.add_argument("filename", type=str, help="путь к файлу с анкетами")
    return parser.parse_args()


def main() -> int:
    """Запустить программу.

    :return: код завершения (0 - успех, 1 - ошибка).
    """
    args = parse_args()

    try:
        text = read_file(args.filename)
    except FileReadError as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1

    top_names = count_names(text).most_common()
    if not top_names:
        print("Валидных анкет не найдено")
        return 0

    for name, count in top_names:
        print(f"{name}: {count}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
