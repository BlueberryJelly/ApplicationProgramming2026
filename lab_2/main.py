"""Скачивание обложек книг с одним из ключевых слов в названии.

Запуск: python main.py --covers_amount ... --keywords ... --covers-out-dir ...
"""

import sys
from lab_2.src.cli import parse_arguments

MAIN_PAGE_URL = "https://books.toscrape.com/"


def main() -> int:
    """Запустить программу.
    
    :return: код завершения (0 - успех, 1 - ошибка).
    """
    covers_amount = parse_arguments().covers_amount
    keywords = parse_arguments().keywords
    covers_out_dir = parse_arguments().covers_out_dir
    print(covers_amount, keywords, covers_out_dir, sep="\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
