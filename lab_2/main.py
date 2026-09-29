"""Скачивание обложек книг с одним из ключевых слов в названии.

Запуск: python main.py --keywords ...
"""

import sys
from src.context import get_args

MAIN_PAGE_REF = "https://books.toscrape.com/"


def main() -> int:
    """Запустить программу.
    
    :return: код завершения (0 - успех, 1 - ошибка).
    """
    keys: list[str] = get_args().keywords
    print(keys, sep="\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
