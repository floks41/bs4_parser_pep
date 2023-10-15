"""Модуль вывода для парсер документации Python."""


import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import BASE_DIR, DATETIME_FORMAT, RESULTS_DIR_NAME
from exceptions import WriteResultsException


def control_output(results, cli_args):
    """Запискает функции вывода результатов работы парсера в соотвествии
    с переданными параметрами командной строки."""
    output = cli_args.output
    if output == 'pretty':
        pretty_output(results)
    elif output == 'file':
        file_output(results, cli_args)
    else:
        default_output(results)


def default_output(results):
    """Вывод данных по умолчанию — в терминал построчно."""
    for row in results:
        print(*row)


def pretty_output(results):
    """Вывод данных в PrettyTable."""
    table = PrettyTable()
    # В качестве заголовков устанавливаем первый элемент списка.
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args):
    """Вывод данных в файл csv."""
    results_dir = BASE_DIR / RESULTS_DIR_NAME
    results_dir.mkdir(exist_ok=True)

    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    # Собираем имя файла из полученных переменных:
    # «режим работы программы» + «дата и время записи» + формат (.csv).
    file_name = f'{parser_mode}_{now_formatted}.csv'
    # Получаем абсолютный путь к файлу с результатами.
    file_path = results_dir / file_name
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, dialect='unix')
            writer.writerows(results)
    except Exception:
        raise WriteResultsException(file_path)
    else:
        logging.info(f'Файл с результатами сохранён: {file_path}')
