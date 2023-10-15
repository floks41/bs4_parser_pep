# Учебный проект парсинга документов PEP — Python Enhancement Proposal (предложений по улучшению Python)

### Разработчик (исполнитель):

👨🏼‍💻Олег: https://github.com/floks41

### Технологии
- Python 3.9
- Beautiful Soup 4.9.3

1. Установка
- Скопировать каталог с проектом в место установки.
- В каталоге проекта установить и запсутить виртуальное окружение:
```
python3 -m venn venv
source venv/bin/activate
```
- Обновить менеджер пакетов PIP и установить зависимости:
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

2. Использование (запуск из командной строки) 

```
Перейти в каталог src
cd src

usage: main.py [-h] [-c] [-o {pretty,file}]
               {whats-new,latest-versions,download}

positional arguments:
  {whats-new,latest-versions,download}
                        Режимы работы парсера

optional arguments:
  -h, --help            show this help message and exit
  -c, --clear-cache     Очистка кеша
  -o {pretty,file}, --output {pretty,file}
                        Дополнительные способы вывода данных
```
3. Функции.
- whats-new: Разбирает станицу изменений в Python.
- latest-versions: Разбирает список версий Python.
- download: Загружает актуальную версию документации последеней версии Python в формате PDF.
- pep: Разбирает список документов PEP (предложений по улучшению Python), подсчитывает количество документов в разрезе их стутусов.

4. Код проекта проверен flake8 после линтинга isort и black:

```
isort src/.
```
```
black src/. --line-length 79 --skip-string-normalization
```