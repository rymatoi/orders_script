import telebot

from db.funcs import add_user, check_user

bot = telebot.TeleBot("5556348629:AAHxKLOq-ZNWILYxx6R_oCEsZ8YuJdtPQbE")


def start_bot():
    """ Запуск бота """
    bot.polling(none_stop=True, interval=0)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    """
    Обработка сообщений
    :param message: сообщение пользователя
    :return:
    """
    if message.text.lower() == "привет":
        bot.send_message(message.from_user.id,
                         format_message("Привет!"))

    elif message.text == "/help":
        bot.send_message(message.from_user.id,
                         format_message(
                             "Доступные команды:\n\n"
                             "/order - подписаться на отслеживание сроков\n"
                             "\n"
                             "Перезапуск бота отключит все активные подписки у всех пользователей."))

    elif message.text == r'/order':
        if check_user(message.from_user.id):
            bot.send_message(message.from_user.id, r"Вы уже оформили подписку!")
        else:
            add_user(message.from_user.id, message.from_user.username)
            bot.send_message(message.from_user.id, r"Поздравляю! Вы подписались на отслеживание заказов.")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


def format_message(message) -> str:
    """
    В конце каждого сообщения бота идет ссылка на /help
    :param message:  сообщение бота
    :return: сообщение бота + шаблон с /help
    """
    message_template = "{0} \n\nДля просмотра всех команд напишите /help."
    return message_template.format(message)
