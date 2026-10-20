"""Обработка изображения:

1) считать изображение из файла;
2) вывести размер изображения;
3) отразить изображение, наложить рамку, сменить цветовые каналы;
4) демонстрация исходного изображения;
5) сохранить преобразованное изображение.

Запуск:
    python main.py input-file output-dir --vertical
    --frame-color --frame-size --channels
"""

import sys
from pathlib import Path

import numpy as np

from src.cli import parse_arguments
from src.io_img import read_img, write_img
from src.plotter import show_img
from src.tr import add_frame, mix_channels, reflect


def main() -> int:
    """Запустить программу.

    :return: код завершения (0 - успех, 1 - ошибка)
    """
    try:
        args = parse_arguments()

        input_file: Path = args.input_file
        img: np.ndarray = read_img(input_file)
        print(img.shape)
        show_img(mix_channels(img))

        vertical: bool = bool(args.vertical)
        img_reflected: np.ndarray = reflect(img, vertical)
        show_img(mix_channels(img_reflected))

        color: tuple[int, int, int] = args.frame_color
        frame: tuple[float, float, float] = args.frame_size
        img_framed: np.ndarray = add_frame(img_reflected, color, frame)
        show_img(mix_channels(img_framed))

        channels: str = args.channels
        img_mixed_channels: np.ndarray = mix_channels(img_framed, channels)
        show_img(img_mixed_channels)

        output_dir: Path = args.output_dir
        output_file: Path = output_dir / f"{input_file.stem} edited{input_file.suffix}"
        write_img(output_file, img_mixed_channels)

    except FileNotFoundError as error:
        print(f"Ошибка: файл не найден или не читается. {error}", file=sys.stderr)
        return 1
    except OSError as error:
        print(f"Ошибка ввода-вывода: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
