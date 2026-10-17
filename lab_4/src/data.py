"""Формирование DataFrame."""

from pathlib import Path

import pandas as pd


def data_from_csv(source: Path) -> pd.DataFrame:
    """Сформировать DataFrame из csv файла.

    Ожидается CSV с двумя колонками: абсолютный и относительный пути.
    Первая строка файла интерпретируется как заголовки и заменяется на
    стандартные имена ["absolute_path", "relative_path"].

    :param source: путь к csv файлу
    :return: данные в виде DataFrame с колонками absolute_path и relative_path
    :raises FileNotFoundError: если файл не найден
    :raises pd.errors.EmptyDataError: если файл пустой
    :raises ValueError: если файл имеет неверную структуру
    """
    if not source.exists():
        raise FileNotFoundError(f"Файл {source} не найден.")
    
    data = pd.read_csv(source, header=0, names=["absolute_path", "relative_path"])
    
    if data.shape[1] != 2:
        raise ValueError(
            f"Файл {source} имеет {data.shape[1]} колонок, ожидается 2."
        )
    
    return data
