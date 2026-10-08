"""Преобразования над изображением: отражение, 
наложение рамки, изменение последовательности каналов"""

import numpy as np

def reflect(img: np.ndarray, vertical: bool = True) -> np.ndarray:
    """Отразить изображение по вертикали или по горизонтали.

    :param img: изображение в виде массива
    :param vertical: если True — отразить по вертикали, иначе по горизонтали
    :return: отражённое изображение
    """
    if vertical:
        return img[::-1, :].copy()
    return img[:, ::-1].copy()
