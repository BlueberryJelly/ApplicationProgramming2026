"""Модуль содержит функции для отражения изображения,
наложения рамки и перестановки цветовых каналов."""

import numpy as np
import cv2

from src.helpers import Color, Frame

COLOR_SPACE = ["RGB", "RBG", "BRG", "BGR", "GBR", "GRB"]
CHANNEL_INDEX = {"B": 0, "G": 1, "R": 2}


def reflect(img: np.ndarray, vertical: bool = True) -> np.ndarray:
    """Отразить изображение по вертикали или по горизонтали.

    :param img: изображение в виде массива
    :param vertical: если True - отразить по вертикали, иначе по горизонтали
    :return: отражённое изображение
    """
    if vertical:
        return img[:, ::-1].copy()
    return img[::-1, :].copy()


def add_frame(img: np.ndarray, color: Color, frame: Frame) -> np.ndarray:
    """Наложить на изображение рамку.

    :param img: изображение в виде массива
    :param color: цвет рамки
    :param frame: отступы рамки
    :return: изображение с наложенной рамкой
    """
    top = int(frame.top * img.shape[0])
    bottom = int(frame.bottom * img.shape[0])
    left = int(frame.left * img.shape[1])
    right = int(frame.right * img.shape[1])
    return cv2.copyMakeBorder(
        img, top, bottom, left, right,
        borderType=cv2.BORDER_CONSTANT,
        value=color.value
    )


def mix_channels(img: np.ndarray, order: str = "RGB") -> np.ndarray:
    """Изменить последовательность каналов изображения.

    :param img: изображение в виде массива
    :param order: целевая последовательность каналов
    :return: изображение с переставленными каналами
    :raises ValueError: недопустимая последовательность каналов
    """
    if order not in COLOR_SPACE:
        raise ValueError(f"Недопустимая последовательность каналов: {order}.")
    indices = [CHANNEL_INDEX[ch] for ch in order]
    return img[:, :, indices].copy()
