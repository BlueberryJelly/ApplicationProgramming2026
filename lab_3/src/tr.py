"""Преобразования над изображением: отражение, 
наложение рамки, изменение последовательности каналов"""

import numpy as np
import cv2

from helpers import Color, Frame


def reflect(img: np.ndarray, vertical: bool = True) -> np.ndarray:
    """Отразить изображение по вертикали или по горизонтали.

    :param img: изображение в виде массива
    :param vertical: если True — отразить по вертикали, иначе по горизонтали
    :return: отражённое изображение
    """
    if vertical:
        return img[::-1, :].copy()
    return img[:, ::-1].copy()


def add_frame(img: np.ndarray, color: Color, frame: Frame) -> np.ndarray:
    """Наложить на изображение рамку.

    :param img: изображение в виде массива
    :param color: цвет рамки
    :param frame: отступы рамки
    :return: изображение с наложенной рамкой
    """
    return cv2.copyMakeBorder(
        img, frame.top, frame.bottom,
        frame.left, frame.right,
        borderType=cv2.BORDER_CONSTANT,
        value=color.value,
    )
