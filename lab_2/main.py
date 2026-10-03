"""Скачивание обложек книг с books.toscrape.com.

Без ключевых слов скачиваются первые обложки каталога, с ключевыми
словами - обложки книг, в названии которых есть хотя бы одно из них.
Рядом с обложками создаётся CSV-аннотация с абсолютными и относительными
путями.

Запуск:
    python main.py --covers-out-dir out
    python main.py --covers-out-dir out --keywords love night
        --covers-amount 10
"""

import logging
import sys

import requests

from src.annotation import write_annotation
from src.cli import parse_arguments
from src.downloader import download_covers
from src.path_iterator import CoverPathIterator
from src.extractor import iter_covers

MAIN_PAGE_URL = "https://books.toscrape.com/"
COVERS_SUBDIR = "covers"
ANNOTATION_FILENAME = "annotation.csv"

logger = logging.getLogger(__name__)


def main() -> int:
    """Запустить программу.

    :return: код завершения (0 - успех, 1 - ошибка или ничего не найдено)
    """
    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s: %(message)s")
    args = parse_arguments()
    out_dir = args.covers_out_dir
    covers_dir = out_dir / COVERS_SUBDIR
    annotation_path = out_dir / ANNOTATION_FILENAME

    try:
        covers_dir.mkdir(parents=True, exist_ok=True)
        covers = iter_covers(MAIN_PAGE_URL, args.keywords)
        paths = download_covers(covers, covers_dir, args.covers_amount)
        write_annotation(paths, out_dir, annotation_path)
    except requests.RequestException as error:
        logger.error("Ошибка сети: %s", error)
        return 1
    except OSError as error:
        logger.error("Ошибка файловой системы: %s", error)
        return 1

    if not paths:
        logger.error("Подходящие обложки не найдены.")
        return 1
    if len(paths) < args.covers_amount:
        logger.warning("Скачано %d из %d запрошенных обложек.",
                       len(paths), args.covers_amount)

    for path in CoverPathIterator(annotation_path):
        print(path)
    logger.info("Аннотация: %s", annotation_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
