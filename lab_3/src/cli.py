"""Разбор аргументов командной строки."""

import argparse
from pathlib import Path


def parse_arguments() -> argparse.Namespace:
    """Разобрать и проверить аргументы командной строки.

    :return: пространство имён с атрибутами img_path, vertical,
             frame_color, frame_size, channels, out_file.
    :raises SystemExit: если переданы некорректные аргументы.
    """
    parser = argparse.ArgumentParser(
        description="Загрузить, изменить изображение, "
                    "согласно атрибутам, и "
                    "сохранить изображение в файл."
    )
    parser.add_argument(
        "img_path", type=Path,
        help="Исходное изображение."
    )
    parser.add_argument(
        "--vertical", type=int, choices=[0, 1], default=1,
        help="1 - отразить по вертикали, 0 - по горизонтали."
    )
    parser.add_argument(
        "--frame-color", nargs=3, type=int, default=[255, 255, 255],
        help="Значение каждого из трёх цветовых каналов в порядке BGR 0-255."
    )
    parser.add_argument(
        "--frame-size", nargs=4, type=float, default=[0.05, 0.05, 0.05, 0.05],
        help="Отступы от краёв в долях от изображения: 4 числа от 0 до 1."
    )
    parser.add_argument(
        "--channels", type=str, default="BGR",
        help="Порядок каналов B, G и R."
    )
    parser.add_argument(
        "out_file", type=Path,
        help="Файл для записи изображения."
    )
    args = parser.parse_args()
    if not args.img_path.exists():
        parser.error(f"Файл {args.img_path} не существует.")
    if not all(0 <= x <= 255 for x in args.frame_color):
        parser.error("--frame-color должен содержать 3 числа от 0 до 255.")
    if not all(0 <= x <= 1 for x in args.frame_size):
        parser.error("--frame-size должен содержать 4 числа от 0 до 1.")
    if sorted(args.channels) != ['B', 'G', 'R']:
        parser.error("--channels должен содержать ровно один раз каждый из символов B, G, R.")
    return args
