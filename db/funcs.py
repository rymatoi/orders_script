from typing import List

from sqlalchemy import bindparam, select

from cbr import get_rub_value
from db import *


def add_user(user_id: str, username: str):
    """
    Добавление пользователя
    :param user_id: id пользователя в Телеграм
    :param username: username пользователя в Телеграм
    """
    engine.execute(SubscribedUser.__table__.insert(), {"id": user_id, "username": username})


def check_user(user_id: str) -> bool:
    """
    Проверка, есть ли пользователь
    :param user_id:  id пользователя в Телеграм

    :returns bool: True если пользователь есть в таблице, False если нет
    """
    res = engine.execute(select([SubscribedUser.__table__]))
    for row in res:
        if str(user_id) == row[0]:
            return True
    return False


def get_users() -> List[SubscribedUser]:
    """
    Возвращает список пользователей
    :return:
    """
    res = engine.execute(select([SubscribedUser.__table__]))
    return res.fetchall()


def bulk_insert(rows):
    """
    Добавляет строки в таблицу order
    :param rows: строки для добавления
    :return:
    """
    insert_rows = _make_order(rows, action='insert')
    if insert_rows:
        engine.execute(Order.__table__.insert(), insert_rows)


def bulk_update(rows):
    """
    Обновляет строки в таблице order
    :param rows: строки для обновления
    :return:
    """
    stmt = Order.__table__.update(). \
        where(Order.id == bindparam('_id')). \
        values({
        'order_number': bindparam('order_number'),
        'price_dollar': bindparam('price_dollar'),
        'date': bindparam('date'),
        'price_rubles': bindparam('price_rubles'),
    })
    update_rows = _make_order(rows, action='update')
    if update_rows:
        engine.execute(stmt, update_rows)


def bulk_delete(rows):
    """
    Удаляет строки из таблицы order
    :param rows: строки для удаления
    :return:
    """
    delete_rows = []
    for row in rows:
        delete_rows.append(row[0])
    engine.execute(Order.__table__.delete().where(Order.__table__.c.id.in_(set(delete_rows))))


def _make_order(rows, action) -> list:
    """
    Делает из строки заказа словарь с ключами-названиями столбцов в таблице order
    :param rows: строки заказов
    :param action: insert/update
    :return:
    """
    result_rows = []
    for row in rows:
        price_rubles = get_rub_value(row[3])
        try:
            result = {
                'id' if action == 'insert' else '_id': int(row[0]),
                'order_number': row[1],
                'price_dollar': float(row[2]),
                'date': row[3],
                'price_rubles': price_rubles * float(row[2])
            }
            result_rows.append(result)
        except Exception as e:
            print(str(e))
    return result_rows
