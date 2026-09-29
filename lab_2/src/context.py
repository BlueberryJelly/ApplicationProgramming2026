'''Получение ключевых слов из аргументов коандной строки'''

import argparse

def get_args() -> argparse.Namespace:
    """Разобрать аргументы командной строки.
    
    :return: пространство имён с атрибутом keywords.
    """
    parser = argparse.ArgumentParser(
        description="Принять ключевые слова для поиска обложек."
    )
    parser.add_argument("--keywords", type=str, nargs="+", 
                        help="Ключевые слова для поиска обложек.")
    return parser.parse_args()
    