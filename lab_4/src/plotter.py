"""Построение графика."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_histogram(data: pd.DataFrame, plot_file: Path) -> None:
    """Построить гистограмму распределения диапазонов по трём каналам (B, G, R).

    :param data: таблица с колонкой ranges (объекты Color)
    :param plot_file: путь для сохранения графика
    """
    b_values = data["ranges"].apply(lambda c: c.blue)
    g_values = data["ranges"].apply(lambda c: c.green)
    r_values = data["ranges"].apply(lambda c: c.red)

    plt.figure(figsize=(10, 6))

    plt.hist(b_values, bins=20, alpha=0.5, color='blue', label='Blue (B)', edgecolor='black')
    plt.hist(g_values, bins=20, alpha=0.5, color='green', label='Green (G)', edgecolor='black')
    plt.hist(r_values, bins=20, alpha=0.5, color='red', label='Red (R)', edgecolor='black')

    plt.title("Распределение диапазонов значений по цветовым каналам")
    plt.xlabel("Диапазон значений (max - min)")
    plt.ylabel("Количество изображений")
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()

    plt.savefig(plot_file, dpi=300)
    plt.show()
