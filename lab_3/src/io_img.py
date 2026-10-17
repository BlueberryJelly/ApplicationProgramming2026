"""Чтение изображения из файла и запись изображения в файл."""

from pathlib import Path

import cv2
import numpy as np


def read_img(source: Path) -> np.ndarray:
    """Считать изображение из файла в массив.

    :param source: путь к файлу для чтения
    :return: изображение в виде массива
    :raises FileNotFoundError: ошибка чтения файла-источника
    """
    img = cv2.imread(source)
    if img is None:
        raise FileNotFoundError(f"Не удалось считать изображение из файла: {source}.")
    return img


def write_img(dest: Path, img: np.ndarray) -> None:
    """Записать изображение из массива в файл.

    :param dest: путь к файлу для записи
    :param img: изображение в виде массива
    :raises OSError: не удалось записать в файл или директория не существует
    """
    parent = dest.parent
    if not parent.exists():
        raise OSError(f"Директория {parent} не существует.")

    if not cv2.imwrite(dest, img):
        raise OSError(f"Не удалось записать изображение в файл: {dest}.")
