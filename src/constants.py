"""Модуль констант для парсер документации Python."""


from pathlib import Path
from urllib.parse import urljoin

BASE_DIR = Path(__file__).parent
MAIN_DOC_URL = 'https://docs.python.org/3/'
WHATS_NEW_PATH = 'whatsnew/'
WHATS_NEW_URL = urljoin(MAIN_DOC_URL, WHATS_NEW_PATH)
PYTHON_VERSIONS_LIST_PATTERN = (
    r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
)
PYTHON_DOC_PDF_A4_URL_PATTERN = r'.+pdf-a4\.zip$'
DOWNLOAD_DIR_NAME = 'downloads'
RESULTS_DIR_NAME = 'results'
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
DOWNLOADS_PATH = 'download.html'
DOWNLOADS_URL = urljoin(MAIN_DOC_URL, DOWNLOADS_PATH)
PEPS_MAIN_URL = 'https://peps.python.org/'
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
UNKNOWN_STATUS_NAME = 'Unknown'
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
LOG_DT_FORMAT = '%d.%m.%Y %H:%M:%S'
