"""Скачивание обложек книг с одним из ключевых слов в названии.

Запуск: python main.py --covers_amount ... --keywords ... --covers-out-dir ...
"""

import sys
from src.context import get_args

MAIN_PAGE_REF = "https://books.toscrape.com/"


def main() -> int:
    """Запустить программу.
    
    :return: код завершения (0 - успех, 1 - ошибка).
    """
    covers_amount = get_args().covers_amount
    keywords = get_args().keywords
    covers_out_dir = get_args().covers_out_dir
    print(covers_amount, keywords, covers_out_dir, sep="\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
