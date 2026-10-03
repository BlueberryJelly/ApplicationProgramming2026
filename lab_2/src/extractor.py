"""Поиск книг и ссылок на их обложки на books.toscrape.com."""

import logging
from collections.abc import Iterator
from dataclasses import dataclass
from urllib.parse import urljoin

import requests

from src.http_client import get_soup

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Book:
    """Книга из списка: полное название и адрес страницы."""

    title: str
    url: str


@dataclass(frozen=True)
class Cover:
    """Обложка: название книги и адрес изображения."""

    title: str
    url: str


def iter_books(start_url: str) -> Iterator[Book]:
    """Обойти все страницы списка и выдавать книги по одной.

    :param start_url: адрес первой страницы списка книг
    :yield: книга (полное название берётся из атрибута title ссылки)
    :raises requests.RequestException: при ошибке загрузки страницы списка
    """
    page_url: str | None = start_url
    while page_url:
        soup = get_soup(page_url)
        for link in soup.select("article.product_pod h3 a"):
            title = str(link.get("title") or link.get_text(strip=True))
            yield Book(title, urljoin(page_url, str(link["href"])))
        next_link = soup.select_one("li.next a")
        page_url = (urljoin(page_url, str(next_link["href"]))
                    if next_link else None)


def matches_keywords(title: str, keywords: list[str]) -> bool:
    """Проверить, содержит ли название хотя бы одно ключевое слово.

    :param title: название книги
    :param keywords: ключевые слова в нижнем регистре; пустой список
        означает «подходит любая книга»
    :return: True, если название подходит
    """
    if not keywords:
        return True
    lowered_title = title.lower()
    return any(keyword in lowered_title for keyword in keywords)


def get_cover_url(book_url: str) -> str:
    """Получить адрес обложки со страницы книги.

    :param book_url: адрес страницы книги
    :return: адрес изображения
    :raises ValueError: если на странице нет обложки
    :raises requests.RequestException: при ошибке загрузки страницы
    """
    image = get_soup(book_url).select_one("#product_gallery img")
    if image is None:
        raise ValueError("на странице нет обложки")
    return urljoin(book_url, str(image["src"]))


def iter_covers(start_url: str, keywords: list[str]) -> Iterator[Cover]:
    """Лениво выдавать обложки книг, подходящих под ключевые слова.

    Страница книги загружается только для подходящих названий.
    Книги с ошибкой пропускаются с предупреждением в лог.

    :param start_url: адрес первой страницы списка книг
    :param keywords: ключевые слова в нижнем регистре (может быть пустым)
    :yield: обложка найденной книги
    """
    for book in iter_books(start_url):
        if not matches_keywords(book.title, keywords):
            continue
        try:
            yield Cover(book.title, get_cover_url(book.url))
        except (requests.RequestException, ValueError) as error:
            logger.warning("Пропуск %s: %s", book.url, error)
