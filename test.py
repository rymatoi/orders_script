import datetime
from functools import lru_cache


# результаты кэшируются, чтобы скрипт не вызывал эту функцию каждые 3 секунды,
# так как во время простоя на вход будут идти одни и те же массивы данных
@lru_cache(maxsize=2)
def match_difference(old_values: tuple, new_values: tuple) -> dict:
    """
    Находит различия между двумя массивами данных.
    Проверяет данные - длина каждой строки должна быть 4 и каждое значение не должно быть None:
    Решает проблему, когда пользователь добавляет запись в таблицу, и заполняет поочереди каждую ячейку.
    Такие строки не будут обрабатываться до того момента, пока пользователь не закончит.
    :param old_values: последнее зафиксированное состояние файла
    :param new_values: состояние с входящими изменениями
    :return: словарь с ключами added, removed, updated, overdue и values
    """

    old_values = {row[0]: row for row in old_values if len(row) == 4 and all(row)}
    new_values = {row[0]: row for row in new_values if len(row) == 4 and all(row)}
    return {
        'added': tuple(new_values[x] for x in new_values if x not in old_values),
        'removed': tuple(old_values[x] for x in old_values if x not in new_values),
        'updated': tuple(new_values[x] for x in new_values if x in old_values and old_values[x] != new_values[x]),
        'overdue': check_dates(new_values),
        'values': tuple(new_values.values())
    }


def check_dates(values) -> tuple:
    """
    Проверяет даты заказов - возвращаются те, у которых срок закончился вчера
    :param values: строки заказов
    :return: просроченные заказы
    """
    overdue_orders = []
    today = datetime.datetime.today()
    for row in values.values():
        try:
            date = datetime.datetime.strptime(row[3], '%d.%m.%Y')
        except:
            date = datetime.datetime.today()
        if (today - date).days == 1:
            overdue_orders.append(row)
    return tuple(overdue_orders)


def format_orders(orders) -> str:
    """ __str__ представление заказов """
    order_template = "№{0}. Заказ {1}\n"
    return ''.join([order_template.format(order[0], order[1]) for order in orders])
