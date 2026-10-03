"""Итератор по путям к файлам обложек."""

import csv
from collections.abc import Iterator
from pathlib import Path

from src.annotation import ABSOLUTE_PATH_COLUMN

IMAGE_SUFFIXES = {".jpg"}


class CoverPathIterator:
    """Итератор по путям к файлам из CSV-аннотации или из папки.

    Одноразовый: после исчерпания нужно создать новый экземпляр.
    """

    def __init__(self, source: Path) -> None:
        """Проверить источник и подготовить обход.

        :param source: путь к CSV-аннотации или к папке с изображениями
        :raises FileNotFoundError: если путь не существует
        :raises ValueError: если путь - не CSV-файл и не папка
        """
        if not source.exists():
            raise FileNotFoundError(f"Путь не существует: {source}")
        if source.is_dir():
            self._paths = self._iter_directory(source)
        elif source.suffix.lower() == ".csv":
            self._paths = self._iter_annotation(source)
        else:
            raise ValueError(f"Неподдерживаемый источник: {source}")

    def __iter__(self) -> "CoverPathIterator":
        """Вернуть сам итератор.

        :return: этот же объект
        """
        return self

    def __next__(self) -> Path:
        """Вернуть следующий путь.

        :return: путь к файлу
        :raises StopIteration: когда пути закончились
        :raises ValueError: если в CSV нет нужной колонки
        """
        return next(self._paths)

    @staticmethod
    def _iter_annotation(annotation_path: Path) -> Iterator[Path]:
        """Читать абсолютные пути из CSV-аннотации.

        :param annotation_path: путь к CSV-файлу
        :yield: путь из колонки absolute_path
        :raises ValueError: если в CSV нет нужной колонки
        """
        with annotation_path.open("r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            if ABSOLUTE_PATH_COLUMN not in (reader.fieldnames or []):
                raise ValueError(
                    f"В аннотации нет колонки '{ABSOLUTE_PATH_COLUMN}'."
                )
            for row in reader:
                raw_path = (row[ABSOLUTE_PATH_COLUMN] or "").strip()
                if raw_path:
                    yield Path(raw_path)

    @staticmethod
    def _iter_directory(folder: Path) -> Iterator[Path]:
        """Рекурсивно обходить изображения в папке.

        :param folder: папка для обхода
        :yield: путь к файлу изображения (в отсортированном порядке)
        """
        for path in folder.rglob("*"):
            if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES:
                yield path
