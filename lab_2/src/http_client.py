"""Загрузка страниц и файлов по HTTP."""

import requests
from bs4 import BeautifulSoup

REQUEST_TIMEOUT = 30
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

_session = requests.Session()
_session.headers["User-Agent"] = USER_AGENT


def get_response(url: str) -> requests.Response:
    """Выполнить GET-запрос и проверить статус ответа.

    :param url: адрес для запроса
    :return: ответ сервера
    :raises requests.RequestException: при ошибке сети или статусе 4xx/5xx
    """
    response = _session.get(url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response


def get_soup(url: str) -> BeautifulSoup:
    """Загрузить страницу и разобрать её HTML.

    :param url: адрес страницы
    :return: дерево разбора страницы
    :raises requests.RequestException: при ошибке загрузки
    """
    content = get_response(url).content
    return BeautifulSoup(content, "html.parser", from_encoding="utf-8")
