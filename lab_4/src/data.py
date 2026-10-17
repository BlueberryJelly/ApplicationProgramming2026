"""Формирование DataFrame."""

from pathlib import Path

import cv2
import numpy as np
import pandas as pd

from ...lab_3.src.io_img import read_img
from ...lab_3.src.helpers import Color


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


def get_img_range(source: Path) -> Color:
    """Вычислить диапазон значений для каждого цветового канала изображения.

    :param source: путь к файлу изображения
    :return: объект Color с диапазонами для каналов B, G, R
    :raises FileNotFoundError: файл не найден
    """
    img = read_img(source)
    b, g, r = cv2.split(img)
    
    b_range = int(np.max(b) - np.min(b))
    g_range = int(np.max(g) - np.min(g))
    r_range = int(np.max(r) - np.min(r))
    
    return Color(b_range, g_range, r_range)


def add_range_column(data: pd.DataFrame) -> pd.DataFrame:
    """Добавить колонку с диапазонами цветовых каналов для каждого изображения.

    :param data: DataFrame с колонкой absolute_path
    :return: новый DataFrame с добавленной колонкой ranges
    :raises KeyError: в DataFrame отсутствует колонка absolute_path
    """
    if "absolute_path" not in data.columns:
        raise KeyError("Отсутствует колонка 'absolute_path'")
    
    return data.assign(ranges=data["absolute_path"].apply(get_img_range))
