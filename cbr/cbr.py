import datetime
from functools import lru_cache

import requests
from lxml import etree


# Результаты для обработанных дат кэшируются, чтобы лишний раз не обращаться к сайту
@lru_cache(maxsize=64)
def get_rub_value(date) -> float:
    """
    Обращается к сайту с курсами валют для получения курса на заданную дату
    :param date: дата, по которой запрашивается курс
    :return: курс в рублях
    """
    result = 0
    today = datetime.datetime.today()
    # Если дата написана с ошибками, то дата устанавливается как сегодняшняя
    # Если дата из будущего, то устанавливается сегодняшняя (так как курс на будущее мы не знаем)
    try:
        _date = datetime.datetime.strptime(date, '%d.%m.%Y')
        if _date > today:
            date = today.strftime('%d.%m.%Y')
    except:
        date = today.strftime('%d.%m.%Y')
    try:
        # Выполняем запрос к API.
        get_xml = requests.get('http://www.cbr.ru/scripts/XML_daily.asp?date_req=%s' % date)
        # Парсинг XML используя ElementTree
        structure = etree.fromstring(get_xml.content)
    except:
        return result

    try:
        # Поиск курса доллара (USD ID: R01235)
        dollar = structure.find("./*[@ID='R01235']/Value")
        result = float(dollar.text.replace(',', '.'))
    except:
        result = 0
    return result
