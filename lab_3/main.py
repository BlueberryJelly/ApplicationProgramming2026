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
from src.helpers import Color, Frame
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
        output_dir: Path = args.output_dir

        output_file: Path = output_dir / f"{input_file.stem} edited{input_file.suffix}"

        vertical: bool = bool(args.vertical)
        color: Color = Color(*args.frame_color)
        frame: Frame = Frame(*args.frame_size)
        channels: str = args.channels

        img: np.ndarray = read_img(input_file)
        print(img.shape)

        img_reflected: np.ndarray = reflect(img, vertical)
        img_framed: np.ndarray = add_frame(img_reflected, color, frame)
        img_mixed_channels: np.ndarray = mix_channels(img_framed, channels)

        show_img(mix_channels(img))
        show_img(mix_channels(img_reflected))
        show_img(mix_channels(img_framed))
        show_img(mix_channels(img_mixed_channels))

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
