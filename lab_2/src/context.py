'''Получение ключевых слов из аргументов коандной строки'''

import argparse

def get_args() -> argparse.Namespace:
    """Разобрать аргументы командной строки.
    
    :return: пространство имён с атрибутами covers_amount keywords covers_out_dir.
    """
    parser = argparse.ArgumentParser(
        description="Принять ключевые слова для поиска обложек."
    )
    parser.add_argument("--covers-amount", type=int, default=30)
    parser.add_argument("--keywords", type=str, nargs="+", 
                        help="Ключевые слова для поиска обложек.")
    parser.add_argument("--covers-out-dir", type=str, required=True,
                       help="Путь к дериктории для сохранения обложек.")
    return parser.parse_args()
    