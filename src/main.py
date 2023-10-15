"""Парсер документации Python."""


import logging
import re
import requests_cache

from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.parse import urljoin

from configs import configure_argument_parser, configure_logging
from constants import (
    BASE_DIR,
    DOWNLOAD_DIR_NAME,
    DOWNLOADS_URL,
    EXPECTED_STATUS,
    MAIN_DOC_URL,
    PEPS_MAIN_URL,
    PYTHON_DOC_PDF_A4_URL_PATTERN,
    PYTHON_VERSIONS_LIST_PATTERN,
    UNKNOWN_STATUS_NAME,
    WHATS_NEW_URL,
)
from exceptions import (
    GetResponseException,
    ParserFindTagException,
    PythonVersionListNotFoundException,
    WriteResultsException,
)
from outputs import control_output
from utils import find_tag, get_response

EXPECTED_STATUS_LIST = tuple(
    item for sublist in EXPECTED_STATUS.values() for item in sublist
)


def get_responce_and_soup(session, url):
    response = get_response(session, url)
    soup = BeautifulSoup(response.text, features='lxml')
    return soup


def whats_new(session):
    """Разбирает станицу изменений в Python."""
    soup = get_responce_and_soup(session, WHATS_NEW_URL)

    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all(
        'li', attrs={'class': 'toctree-l1'}
    )

    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    for section in tqdm(sections_by_python):
        version_a_tag = section.find('a')
        version_link = urljoin(WHATS_NEW_URL, version_a_tag['href'])

        soup = get_responce_and_soup(session, version_link)

        h1_tag = find_tag(soup, 'h1')
        article_title = h1_tag.text.replace('¶', ' ')
        dl = find_tag(soup, 'dl')

        author_editor = dl.text.replace('\n', ' ')
        results.append((version_link, article_title, author_editor))

    return results


def latest_versions(session):
    """Разбирает список версий Python."""
    soup = get_responce_and_soup(session, MAIN_DOC_URL)
    sidebar = find_tag(soup, 'div', attrs={'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    results = [('Ссылка на документацию', 'Версия', 'Статус')]

    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise PythonVersionListNotFoundException(MAIN_DOC_URL)

    for a_tag in tqdm(a_tags):
        link = a_tag['href']
        text_match = re.search(PYTHON_VERSIONS_LIST_PATTERN, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''

        results.append((link, version, status))
    return results


def download(session):
    """Загружает актуальную версию документации
    последеней версии Python в формате PDF."""
    soup = get_responce_and_soup(session, DOWNLOADS_URL)

    main_tag = find_tag(soup, 'div', attrs={'role': 'main'})
    table_tag = find_tag(main_tag, 'table', attrs={'class': 'docutils'})
    pdf_a4_tag = find_tag(
        table_tag,
        'a',
        attrs={'href': re.compile(PYTHON_DOC_PDF_A4_URL_PATTERN)},
    )
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(MAIN_DOC_URL, pdf_a4_link)
    filename = archive_url.split('/')[-1]

    downloads_dir = BASE_DIR / DOWNLOAD_DIR_NAME
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename

    response = get_response(session, archive_url)
    try:
        with open(archive_path, 'wb') as file:
            file.write(response.content)
    except Exception:
        raise WriteResultsException(archive_path)
    else:
        logging.info(f'Архив был загружен и сохранён: {archive_path}')


def pep(session):
    """Разбирает список документов PEP (предложений по улучшению Python),
    подсчитывает количество документов в разрезе их стутусов."""
    soup = get_responce_and_soup(session, PEPS_MAIN_URL)
    # print(soup)
    # soup.findNextSibling
    section_tag = find_tag(
        soup=soup, tag='section', attrs={'id': 'numerical-index'}
    )
    table_tag = find_tag(
        section_tag, 'table', attrs={'class': 'pep-zero-table'}
    )
    tbody_tag = find_tag(table_tag, 'tbody')
    row_tags = tbody_tag.find_all('tr')

    pep_list = []
    freq_dict = {}

    for row in tqdm(row_tags):
        td_tag = find_tag(row, 'td')
        pep_keys = find_tag(td_tag, 'abbr').text
        pep_status_key = pep_keys[1:]
        pep_url = urljoin(PEPS_MAIN_URL, find_tag(row, 'a')['href'])
        pep_list.append((pep_status_key, pep_url))

        soup = get_responce_and_soup(session, pep_url)

        section_tag = find_tag(soup, 'section', attrs={'id': 'pep-content'})
        dl_tag = find_tag(section_tag, 'dl')
        status_word_string = find_tag(
            dl_tag, None, string='Status', mode='child'
        )
        dd_tag = find_tag(status_word_string.parent, 'dd', mode='next_sibling')
        status_text = find_tag(dd_tag, 'abbr').text

        if status_text not in EXPECTED_STATUS.get(pep_status_key):
            current_expected_statuses = ', '.join(
                EXPECTED_STATUS.get(pep_status_key)
            )
            logging.info(
                f'Несовпадающие статусы: {pep_url}. '
                f'Статус в карточке: {status_text}. '
                f'Ожидаемые статусы: {current_expected_statuses}.'
            )

        if status_text not in EXPECTED_STATUS_LIST:
            status_text = UNKNOWN_STATUS_NAME

        if freq_dict.get(status_text) is not None:
            freq_dict[status_text] += 1
        else:
            freq_dict[status_text] = 1

    total_peps_number = 0
    results = [
        ('Статус', 'Количество'),
    ]

    for key, value in freq_dict.items():
        results.append((key, value))
        total_peps_number += value
    results.append(('Total', total_peps_number))

    return results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    """Главная функция модуля, в ней осуществляется настройка логирования,
    разбор аргументов командной строки, запуск нужного парсера, отправка
    результатов для вывода."""
    configure_logging()

    logging.info('Парсер запущен!')

    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()

    logging.info(f'Аргументы командной строки: {args}')

    session = requests_cache.CachedSession()

    if args.clear_cache:
        session.cache.clear()

    parser_mode = args.mode

    try:
        results = MODE_TO_FUNCTION[parser_mode](session)
    except (
        ParserFindTagException,
        GetResponseException,
        WriteResultsException,
        PythonVersionListNotFoundException,
    ) as parser_exception:
        logging.error(parser_exception.error_msg)

    except Exception as exception:
        logging.exception(
            f'В работе парсера возникла ошибка {str(exception)}',
            stack_info=True,
        )
    else:
        if results is not None:
            control_output(results, args)

    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
