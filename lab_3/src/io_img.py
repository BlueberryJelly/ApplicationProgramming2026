"""Чтение изображения из файла и запись изображения в файл."""

from pathlib import Path
import cv2
import numpy as np

ALLOWED_EXTENSIONS = [".jpg"]


def read_img(source: Path) -> np.ndarray:
    """Считать изображение из файла в массив.

    :param source: путь к файлу для чтения
    :return img: изображение в виде массива
    :raises ValueError: недопустимое расширение файла-источника
    :raises FileNotFoundError: ошибка чтения файла-источника
    """
    if source.suffix not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Недопустимое расширение файла-источника: {source.suffix}.")
    img = cv2.imread(source)
    if img is None:
        raise FileNotFoundError(f"Не удалось считать изображение из файла: {source}.")
    return img


def write_img(dest: Path, img: np.ndarray) -> None:
    """Записать изображение из массива в файл.

    :param dest: путь к файлу для записи
    :param img: изображение в виде массива
    :raises ValueError: недопустимое расширение файла для записи
    :raises OSError: ошибка записи в файл
    """
    if dest.suffix not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Недопустимое расширение файла для записи: {dest.suffix}.")
    if not cv2.imwrite(dest, img):
        raise OSError(f"Не удалось записать изображение в файл: {dest}.")
