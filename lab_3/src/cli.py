"""Разбор аргументов командной строки."""

import argparse
from pathlib import Path

ALLOWED_EXTENSIONS = [".jpg"]


def parse_arguments() -> argparse.Namespace:
    """Разобрать и проверить аргументы командной строки.

    :return: пространство имён с атрибутами input_file, output_dir,
             vertical, frame_color, frame_size, channels.
    :raises SystemExit: если переданы некорректные аргументы.
    """
    parser = argparse.ArgumentParser(
        description="Загрузить, изменить изображение "
        "согласно атрибутам и "
        "сохранить изображение в директорию."
    )
    parser.add_argument("input_file", type=Path, help="Путь к изображению.")
    parser.add_argument("output_dir", type=Path, help="Директория для записи изображения.")
    parser.add_argument(
        "--vertical",
        type=int,
        choices=[0, 1],
        default=1,
        help="1 - отразить по вертикали, 0 - по горизонтали.",
    )
    parser.add_argument(
        "--frame-color",
        nargs=3,
        type=int,
        default=[255, 255, 255],
        help="Значение каждого из трёх цветовых каналов в порядке BGR 0-255.",
    )
    parser.add_argument(
        "--frame-size",
        nargs=4,
        type=float,
        default=[0.05, 0.05, 0.05, 0.05],
        help="Отступы от краёв в долях от изображения: 4 числа от 0 до 1.",
    )
    parser.add_argument(
        "--channels", type=str, default="BGR", help="Порядок каналов B, G и R."
    )
    args = parser.parse_args()

    if not args.input_file.exists():
        parser.error(f"Путь {args.input_file} не существует.")
    if args.input_file.suffix.lower() not in ALLOWED_EXTENSIONS:
        parser.error(
            f"Файл {args.input_file} имеет недопустимое расширение. "
            f"Ожидается: {ALLOWED_EXTENSIONS}"
        )

    if not args.output_dir.exists():
        args.output_dir.mkdir(parents=True, exist_ok=True)
    elif not args.output_dir.is_dir():
        parser.error(f"Путь {args.output_dir} существует, но не является директорией.")

    if not all(0 <= x <= 255 for x in args.frame_color):
        parser.error("--frame-color должен содержать 3 числа от 0 до 255.")

    if not all(0 <= x <= 1 for x in args.frame_size):
        parser.error("--frame-size должен содержать 4 числа от 0 до 1.")

    if sum(args.frame_size) > 1.0:
        parser.error("Сумма отступов --frame-size не должна превышать 1.0.")

    if set(args.channels) != {"B", "G", "R"} or len(args.channels) != 3:
        parser.error(
            "--channels должен содержать ровно один раз каждый из символов B, G, R."
        )

    return args
