"""Модуль функций-утилит для парсер документации Python."""


from bs4 import BeautifulSoup
from requests import RequestException

from exceptions import GetResponseException, ParserFindTagException


def get_response(session, url):
    """Перехватывает ошибки RequestException.
    Загружает страницу URL c использование session из аргументов.
    Возвражае объект Response.
    В случае неудачной загрузки страницы, логирует ошибку, возвращает None.
    """
    try:
        response = session.get(url)
    except RequestException:
        raise GetResponseException(url)
    response.encoding = 'utf-8'
    return response


def find_tag(
    soup: BeautifulSoup, tag=None, attrs=None, string=None, mode='find'
):
    """Перехват ошибки поиска тегов.
    Осуществляет поиск тега tag в объекте soup с атрибутами из словаря attrs
    (не обязательный аргумент), строкой string. Вызывает для воиска методы
    объекта BeautifulSoup soup     в зависимости от аргумента mode:
    find - soup.find, child - soup.findChild,
    next_sibling - soup.find_next_sibling.  Если тег не найден, логирует
    ошибку, вызывает исключение ParserFindTagException.
    """
    function_mode = {
        'find': soup.find,
        'child': soup.findChild,
        'next_sibling': soup.find_next_sibling,
    }
    searched_tag = function_mode[mode](
        name=(tag or None), attrs=(attrs or {}), string=(string or None)
    )
    if searched_tag is None:
        raise ParserFindTagException(tag, attrs)
    return searched_tag
