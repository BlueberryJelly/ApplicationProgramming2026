import argparse
import pathlib

def get_data() -> str:
    """
    Получает путь к файлу из аргументов командной строки.
    Записывает данные из файла в переменную.
    :return text: данные считанные из файла.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-path", type=pathlib.Path)
    args = parser.parse_args()

    if not args.data_path.exists():
        raise SystemExit(f"Входные данные не найдены: {args.data_path} не содержит источник.")

    with args.data_path.open(mode="r", encoding="utf-8") as file:
        text = file.read()

    return text
