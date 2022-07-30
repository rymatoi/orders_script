""" Главный модуль программы """

import time

import db.funcs as session
from google_drive_api import google_sheets as gs
from telegram_bot.bot import start_bot, bot
from test import match_difference, format_orders

import multiprocessing as mp

if __name__ == '__main__':
    """ Точка входа в программу """
    # Запускаем бота
    mp.Process(target=start_bot).start()

    # old_values будет хранить текущее состояние таблицы на гугл диске
    # overdue_notified - те записи, о которых уже уведомили пользователей телеграм, подписанных на отслеживание заказов
    # overdue_notified нужен для того, чтобы дублировать уведомления
    notified = False
    old_values = tuple()
    overdue_notified = tuple()
    while True:
        # match_difference фильтрует записи (плохие отбрасывает), и находит изменения.
        different_rows = match_difference(old_values, gs.get_values())
        if different_rows['added'] or different_rows['updated'] or different_rows['removed']:
            # если есть изменения, то вносятся правки в базу данных
            session.bulk_insert(different_rows['added'])
            session.bulk_update(different_rows['updated'])
            session.bulk_delete(different_rows['removed'])
            # а в old_values кладется обработанный набор данных
            old_values = different_rows['values']

        # если есть просроченные заказы, то пользователям посылаются уведомления
        if different_rows['overdue']:
            users = session.get_users()
            need_notify = tuple(x for x in different_rows["overdue"] if x not in overdue_notified)
            if need_notify:
                for user in users:
                    # need_notify - те заказы, которые просрочены, но еще не отправлялись как уведомления
                    # точно так же, как мы уведомляем о просрочках, можно уведомлять о всех изменениях в файле..
                    bot.send_message(user.id,
                                     f'У следующих заказов вчера прошел срок:\n'
                                     f'{format_orders(need_notify)}')
                    notified = True
                if notified:
                    overdue_notified += need_notify
                    notified = False

        # скрипт проверяет файл каждые 3 секунды
        time.sleep(3)
