"""Разбор аргументов командной строки."""

import argparse
from pathlib import Path

DEFAULT_COVERS_AMOUNT = 30


def parse_arguments() -> argparse.Namespace:
    """Разобрать и проверить аргументы командной строки.

    :return: пространство имён с атрибутами covers_amount, keywords,
        covers_out_dir; keywords - список слов в нижнем регистре.
    """
    parser = argparse.ArgumentParser(
        description="Скачивание обложек книг с books.toscrape.com. "
                    "Cкачиваются обложки книг, "
                    "в названии которых есть хотя бы одно из ключевых слов."
    )
    parser.add_argument(
        "--covers-amount", type=int, default=DEFAULT_COVERS_AMOUNT,
        help=f"Сколько обложек скачать (по умолчанию {DEFAULT_COVERS_AMOUNT})."
    )
    parser.add_argument(
        "--keywords", nargs="+", type=str,
        help="Одно или несколько ключевых слов для поиска в названии."
    )
    parser.add_argument(
        "--covers-out-dir", type=Path, required=True,
        help="Папка для обложек и CSV-аннотации (создаётся при отсутствии)."
    )
    args = parser.parse_args()

    if args.covers_amount <= 0:
        parser.error("--covers-amount должен быть положительным числом.")
    if args.covers_out_dir.exists() and not args.covers_out_dir.is_dir():
        parser.error("--covers-out-dir должен быть директорией.")

    args.keywords = [word.strip().lower() for word in args.keywords
                     if word.strip()]
    return args
