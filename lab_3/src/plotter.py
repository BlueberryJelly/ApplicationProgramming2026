"""Демонастрация изображения."""

import matplotlib.pyplot as plt
import numpy as np

def show_img(img: np.ndarray) -> None:
    """Показать изображение в окне.
    
    :param img: изображение в виде массива
    """
    plt.imsave(img)
    plt.show()
