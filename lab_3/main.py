"""Обработка изображения:

1) считать изображение из файла;
2) вывести размер изображения;
3) отразить изображение, наложить рамку, сменить цветовые каналы;
4) демонстрация исходного изображения;
5) сохранить преобразованное изображение.

Запуск:
    python main.py img-path --vertical --frame-color
        --frame-size --channels out-dir
"""

from pathlib import Path
import sys
import numpy as np

from src.cli import parse_arguments
from src.helpers import Color, Frame
from src.io_img import read_img, write_img
from src.tr import reflect, add_frame, mix_channels
from src.plotter import show_img

def main() -> int:
    """Запустить программу.
    
    :return: код завершения (0 - успех, 1 - ошибка или ничего не найдено)
    """
    args = parse_arguments()
    img_path: Path = args.img_path
    vertical: bool = bool(args.vertical)
    color: Color = Color(*args.frame_color)
    frame: Frame = Frame(*args.frame_size)
    channels: str = args.channels
    out_file: Path = args.out_file

    img: np.ndarray = read_img(img_path)
    print(img.shape)
    img_reflected: np.ndarray = reflect(img, vertical)
    img_framed: np.ndarray = add_frame(img_reflected, color, frame)
    img_mixed_channels: np.ndarray = mix_channels(img_framed, channels)
    show_img(mix_channels(img))
    show_img(mix_channels(img_reflected))
    show_img(mix_channels(img_framed))
    show_img(mix_channels(img_mixed_channels))
    write_img(out_file, img_mixed_channels)
    return 0


if __name__ == "__main__":
    sys.exit(main())
