"""Модуль констант для парсер документации Python."""


from pathlib import Path
from urllib.parse import urljoin

BASE_DIR = Path(__file__).parent
MAIN_DOC_URL = 'https://docs.python.org/3/'
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
DOWNLOADS_PATH = 'download.html'
DOWNLOADS_URL = urljoin(MAIN_DOC_URL, DOWNLOADS_PATH)
DOWNLOAD_DIR_NAME = 'downloads'
EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}
LI_ALL_VERSIONS_TEXT_PATTERN = r'.*All versions.*'
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
LOG_DT_FORMAT = '%d.%m.%Y %H:%M:%S'
PEPS_MAIN_URL = 'https://peps.python.org/'
PYTHON_VERSIONS_LIST_PATTERN = (
    r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
)
PYTHON_DOC_PDF_A4_URL_PATTERN = r'.+pdf-a4\.zip$'
RESULTS_DIR_NAME = 'results'
RESULT_HEADERS_TUPLES = {
    'whats-new': ('Ссылка на статью', 'Заголовок', 'Редактор, Автор'),
    'latest-versions': ('Ссылка на документацию', 'Версия', 'Статус'),
    'pep': ('Статус', 'Количество'),
}
WHATS_NEW_PATH = 'whatsnew/'
WHATS_NEW_URL = urljoin(MAIN_DOC_URL, WHATS_NEW_PATH)
UNKNOWN_STATUS_NAME = 'Unknown'
