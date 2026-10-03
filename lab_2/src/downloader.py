"""Скачивание обложек в локальную папку."""

import logging
import re
from collections.abc import Iterable
from pathlib import Path

import requests

from src.http_client import get_response
from src.extractor import Cover

logger = logging.getLogger(__name__)

DEFAULT_SUFFIX = ".jpg"
MAX_FILENAME_LENGTH = 120


def make_safe_filename(title: str,
                       max_length: int = MAX_FILENAME_LENGTH) -> str:
    """Убрать из названия символы, недопустимые в именах файлов.

    :param title: название книги
    :param max_length: максимальная длина имени без расширения
    :raises ValueError: недопустимая длина имени файла без расширения
    :return: безопасное имя файла без расширения
    """
    if max_length <= 0:
        raise ValueError("недопустимая длина имени файла без расширения.")
    name = re.sub(r'[\\/:*?"<>|]+', "_", title).strip(" .")
    return name[:max_length] or "cover"


def make_unique_path(folder: Path, stem: str, suffix: str) -> Path:
    """Подобрать несуществующий путь, добавляя номер при совпадении имён.

    :param folder: папка для файла
    :param stem: имя файла без расширения
    :param suffix: расширение с точкой
    :return: путь к ещё не существующему файлу
    """
    path = folder / f"{stem}{suffix}"
    counter = 2
    while path.exists():
        path = folder / f"{stem}_{counter}{suffix}"
        counter += 1
    return path


def download_cover(cover: Cover, folder: Path) -> Path:
    """Скачать одну обложку в папку.

    :param cover: обложка (название и адрес изображения)
    :param folder: папка для сохранения
    :return: путь к сохранённому файлу
    :raises requests.RequestException: при ошибке скачивания
    :raises OSError: при ошибке записи файла
    """
    suffix = Path(cover.url).suffix or DEFAULT_SUFFIX
    content = get_response(cover.url).content
    path = make_unique_path(folder, make_safe_filename(cover.title), suffix)
    path.write_bytes(content)
    return path


def download_covers(covers: Iterable[Cover], folder: Path,
                    limit: int) -> list[Path]:
    """Скачивать обложки, пока не наберётся нужное количество.

    Неудачные загрузки пропускаются и не засчитываются в лимит.

    :param covers: обложки (желательно ленивый итератор)
    :param folder: существующая папка для сохранения
    :param limit: сколько файлов нужно скачать
    :return: пути к скачанным файлам (может быть меньше limit,
        если подходящих обложек не хватило)
    """
    paths: list[Path] = []
    for cover in covers:
        try:
            paths.append(download_cover(cover, folder))
        except (requests.RequestException, OSError) as error:
            logger.warning("Не скачана «%s»: %s", cover.title, error)
            continue
        logger.info("Скачано %d/%d: %s", len(paths), limit, paths[-1].name)
        if len(paths) >= limit:
            break
    return paths
