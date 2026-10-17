"""Разбор аргументов командной строки."""

import argparse
from pathlib import Path

ALLOWED_EXTENSIONS = [".csv"]


def parse_arguments() -> argparse.Namespace:
    """Разобрать и проверить аргументы командной строки.

    :return: пространство имён с атрибутами input_file, output_dir, result_name
    """
    parser = argparse.ArgumentParser(
        description="Загрузить аннотацию, "
        "выполнить преобразования, "
        "отобразить гистограмму и "
        "сохранить результат."
    )
    parser.add_argument("input_file", type=Path, help="Путь к аннотации.")
    parser.add_argument("output_dir", type=Path, help="Директория для сохранения результата.")
    parser.add_argument("--result-name", type=Path, help="Имя для файла с результатом.")
    
    args = parser.parse_args()
    
    if not args.input_file.exists():
        parser.error(f"Путь {args.input_file} не существует.")
    if args.input_file.suffix not in ALLOWED_EXTENSIONS:
        parser.error(f"Файл {args.input_file} имеет недопустимое расширение. Ожидается: {ALLOWED_EXTENSIONS}")
        
    if not args.output_dir.exists():
        args.output_dir.mkdir(parents=True, exist_ok=True)
    elif not args.output_dir.is_dir():
        parser.error(f"Путь {args.output_dir} существует, но не является директорией.")
    
    if args.result_name and args.result_name.suffix not in ALLOWED_EXTENSIONS:
        parser.error(f"Файл результата {args.result_name} имеет недопустимое расширение.")

    return args