'''Получение ключевых слов из аргументов коандной строки'''

import argparse
from pathlib import Path


def parse_arguments() -> argparse.Namespace:
    """Разбор и проверка аргументов командной строки.
    
    :return: пространство имён с атрибутами covers_amount keywords covers_out_dir.
    """
    parser = argparse.ArgumentParser(description="Загрузка обложек книг, при наличии ключевого слова в названии.")
    parser.add_argument("--covers-amount", type=int, default=30,
        help="Число скачиваемых обложек (30, по-умолчанию).")
    parser.add_argument("--keywords", type=str, nargs="+",
        help="Не менее одного ключевого слова.")
    parser.add_argument("--covers-out-dir", type=Path, required=True,
        help="Путь для сохранения обложек и CSV аннотации.")
    args = parser.parse_args()

    if args.covers_amount <= 0:
        parser.error("--covers-amount должно быть положительным числом.")

    args.keywords = [keyword.strip().lower() for keyword in args.keywords if keyword.strip()]

    if not (args.covers_out_dir.exists(follow_symlinks=False) and
            args.covers_out_dir.is_dir(follow_symlinks=False)):
        parser.error("--covers-out-dir должен существовать и быть директорией")

    return args
