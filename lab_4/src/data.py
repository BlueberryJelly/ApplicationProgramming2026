"""Формирование DataFrame."""

from pathlib import Path

import cv2
import numpy as np
import pandas as pd


def data_from_csv(source: Path) -> pd.DataFrame:
    """Сформировать DataFrame из csv файла.

    Ожидается CSV с двумя колонками: абсолютный и относительный пути.
    Первая строка файла интерпретируется как заголовки и заменяется на
    стандартные имена ["absolute_path", "relative_path"].

    :param source: путь к csv файлу
    :return: данные в виде DataFrame с колонками absolute_path и relative_path
    :raises FileNotFoundError: файл не найден
    """
    if not source.exists():
        raise FileNotFoundError(f"Файл {source} не найден.")

    data = pd.read_csv(source, header=0, names=["absolute_path", "relative_path"])

    return data


def get_img_range(source: Path) -> tuple[int, int, int]:
    """Вычислить диапазон значений для каждого цветового канала изображения.

    :param source: путь к файлу изображения
    :return: кортеж с диапазонами для каналов B, G, R
    :raises FileNotFoundError: файл не найден или не является изображением
    """
    img = cv2.imread(source)
    if img is None:
        raise FileNotFoundError(f"Не удалось считать изображение из файла: {source}.")

    b, g, r = img[:, :, 0], img[:, :, 1], img[:, :, 2]

    b_range = int(np.max(b) - np.min(b))
    g_range = int(np.max(g) - np.min(g))
    r_range = int(np.max(r) - np.min(r))

    return b_range, g_range, r_range


def add_range_column(data: pd.DataFrame) -> pd.DataFrame:
    """Добавить колонку с диапазонами цветовых каналов для каждого изображения.

    :param data: DataFrame с колонкой absolute_path
    :return: новый DataFrame с добавленной колонкой ranges
    :raises KeyError: в DataFrame отсутствует колонка absolute_path
    """
    if "absolute_path" not in data.columns:
        raise KeyError("Отсутствует колонка 'absolute_path'")

    return data.assign(ranges=data["absolute_path"].apply(get_img_range))


def sort_by_ranges(data: pd.DataFrame, ascending: bool = True) -> pd.DataFrame:
    """Отсортировать DataFrame по колонке ranges.

    Сортировка лексикографическая: сначала по диапазону канала B,
    затем G, затем R (так как ranges — это кортеж из трёх чисел).

    :param data: DataFrame с колонкой ranges
    :param ascending: если True — по возрастанию, иначе по убыванию
    :return: новый DataFrame, отсортированный по колонке ranges
    :raises KeyError: в DataFrame отсутствует колонка ranges
    """
    if "ranges" not in data.columns:
        raise KeyError("Отсутствует колонка 'ranges'")

    return data.sort_values("ranges", ascending=ascending)


def filter_by_ranges(
    data: pd.DataFrame,
    min_range: tuple[int, int, int],
    max_range: tuple[int, int, int],
) -> pd.DataFrame:
    """Отфильтровать DataFrame по диапазонам цветовых каналов.

    Оставляет только те строки, где все три канала (B, G, R) находятся
    в пределах [min_range, max_range] включительно.

    :param data: DataFrame с колонкой ranges
    :param min_range: минимальные значения для каналов B, G, R
    :param max_range: максимальные значения для каналов B, G, R
    :return: новый DataFrame с отфильтрованными строками
    :raises KeyError: в DataFrame отсутствует колонка ranges
    :raises ValueError: min_range больше max_range хотя бы для одного канала
    """
    if "ranges" not in data.columns:
        raise KeyError("Отсутствует колонка 'ranges'")

    if any(mn > mx for mn, mx in zip(min_range, max_range)):
        raise ValueError("Минимальное значение не должно превосходить максимальное.")

    mask = data["ranges"].apply(
        lambda r: all(mn <= val <= mx for val, mn, mx in zip(r, min_range, max_range))
    )

    return data[mask]
