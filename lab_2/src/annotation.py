"""Запись CSV-аннотации к скачанным файлам."""

import csv
from collections.abc import Iterable
from pathlib import Path

ABSOLUTE_PATH_COLUMN = "absolute_path"
RELATIVE_PATH_COLUMN = "relative_path"


def write_annotation(paths: Iterable[Path], base_dir: Path,
                     annotation_path: Path) -> None:
    """Сохранить абсолютные и относительные пути файлов в CSV.

    :param paths: пути к файлам, лежащим внутри base_dir
    :param base_dir: папка, от которой считаются относительные пути
    :param annotation_path: путь к создаваемому CSV-файлу
    :raises ValueError: если файл лежит вне base_dir
    :raises OSError: при ошибке записи .jpg
    """
    base_dir = base_dir.resolve()
    with annotation_path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([ABSOLUTE_PATH_COLUMN, RELATIVE_PATH_COLUMN])
        for path in paths:
            absolute = path.resolve()
            writer.writerow([absolute, absolute.relative_to(base_dir)])
