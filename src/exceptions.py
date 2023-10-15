"""Модуль исключений для парсер документации Python."""


class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""

    def __init__(self, tag, attrs) -> None:
        self.error_msg = f'Не найден тег {tag} {attrs}'
        super().__init__(self.error_msg)


class GetResponseException(Exception):
    """Вызывается при неудачной загрузке страницы."""

    def __init__(self, url) -> None:
        self.error_msg = f'Возникла ошибка при загрузке страницы {url}'
        super().__init__(self.error_msg)


class WriteResultsException(Exception):
    """Вызывается при неудачной записи результатов в файл."""

    def __init__(self, path) -> None:
        self.error_msg = f'Не удалось записать файл {path}'
        super().__init__(self.error_msg)


class PythonVersionListNotFoundException(Exception):
    """Вызывается, когда на странице документации не найден
    список последний версий Python."""

    def __init__(self, url) -> None:
        self.error_msg = f'Список версий Python на странице {url} не найден.'
        super().__init__(self.error_msg)
