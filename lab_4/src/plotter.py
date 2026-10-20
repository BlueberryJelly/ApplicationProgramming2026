"""Построение графика."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_histogram(data: pd.DataFrame, plot_file: Path) -> None:
    """Построить график с тремя кривыми распределения по каналам (B, G, R).

    :param data: таблица с колонкой ranges (объекты Color)
    :param plot_file: путь для сохранения графика
    """
    blue, green, red = range(3)
    b_values = data["ranges"].apply(lambda c: c[blue])
    g_values = data["ranges"].apply(lambda c: c[green])
    r_values = data["ranges"].apply(lambda c: c[red])

    plt.figure(figsize=(10, 6))

    plt.hist(
        b_values,
        bins=20,
        histtype="step",
        color="blue",
        linewidth=2,
        label="Blue (B)",
        density=True,
    )
    plt.hist(
        g_values,
        bins=20,
        histtype="step",
        color="green",
        linewidth=2,
        label="Green (G)",
        density=True,
    )
    plt.hist(
        r_values,
        bins=20,
        histtype="step",
        color="red",
        linewidth=2,
        label="Red (R)",
        density=True,
    )

    plt.title("Распределение диапазонов значений по цветовым каналам")
    plt.xlabel("Диапазон значений (max - min)")
    plt.ylabel("Плотность распределения")
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()

    plt.savefig(plot_file, dpi=300)
    plt.show()
