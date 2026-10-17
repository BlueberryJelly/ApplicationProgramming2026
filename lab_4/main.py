"""Обработка DataFrame:

1) сформировать DataFrame из csv аннотации;
2) произвести именование колонок;
3) добавить новую колонку с диапазонами для каждого цветового канала;
4) отсортировать DataFrame по добавленной колонке;
5) отфильровать DataFrame по добавленной колонке;
6) создать и отобразить гистограмму по добавленной колонке для всех отсортированных данных
7) сохранить DataFrame и гистограмму.

Запуск:
    python main.py input-file output-dir --result-name
"""

import sys
from pathlib import Path

import pandas as pd

from src.cli import parse_arguments
from src.data import data_from_csv, add_range_column, sort_by_ranges, filter_by_ranges
from src.plotter import plot_histogram

PLOT_EXTENSION: str = ".jpg"
MIN_RANGE: tuple[int, int, int] = (220, 220, 220)
MAX_RANGE: tuple[int, int, int] = (255, 250, 250)


def main() -> int:
    """Запустить программу.

    :return: код завершения (0 - успех, 1 - ошибка)
    """
    try:
        args = parse_arguments()
        input_file: Path = args.input_file

        data: pd.DataFrame = data_from_csv(input_file)

        if data.empty:
            print("Аннотация пуста.")
            return 1

        print("Искодный DataFrame:")
        print(data)

        extended_data: pd.DataFrame = add_range_column(data)
        print("DataFrame с колонкой диапазонов цветовых каналов:")
        print(extended_data)

        sorted_data: pd.DataFrame = sort_by_ranges(extended_data)
        print("DataFrame отсортированный по колонке диапазонов цветовых каналов:")
        print(sorted_data)

        filtered_data: pd.DataFrame = filter_by_ranges(sorted_data, MIN_RANGE, MAX_RANGE)
        print("DataFrame отфильтрованный по колонке диапазонов цветовых каналов:")
        print(filtered_data)

        output_dir: Path = args.output_dir
        result_name: Path = args.result_name

        plot_file: Path = output_dir / f"{result_name.stem}{PLOT_EXTENSION}"
        plot_histogram(sorted_data, plot_file)

        output_file: Path = output_dir / result_name
        sorted_data.to_csv(output_file, index=False)

    except FileNotFoundError as error:
        print(f"Ошибка: файл не найден. {error}", file=sys.stderr)
        return 1
    except KeyError as error:
        print(f"Ошибка: в данных нет нужной колонки. {error.args[0]}", file=sys.stderr)
        return 1
    except ValueError as error:
        print(f"Ошибка в значениях данных или параметров: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
