"""Формирование DataFrame."""

from pathlib import Path

import pandas as pd


def data_from_csv(source: Path) -> pd.DataFrame:
    """Сформировать DataFrame из csv файла.

    :param source: путь к csv файлу
    :return: данные в виде DataFrame
    :raises FileNotFoundError: если файл не найден
    :raises pd.errors.EmptyDataError: если файл пустой
    """
    if not source.exists():
        raise FileNotFoundError(f"Файл {source} не найден.")
    
    data = pd.read_csv(source)
    return data
