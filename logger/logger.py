from datetime import datetime as dt
import sqlite3


class Logger:
    def __init__(self, db_filepath: str, txt_filepath: str):
        self.dbFilepath = db_filepath
        self.txtFilepath = txt_filepath

        self.log_to_txt(f"{'-' * 30} ЗАПУСК ОТ {dt.today().strftime('%d.%m.%Y')} {'-' * 30}", False)
        self.log_to_db(f"{'*' * 5} ЗАПУСК ОТ {dt.today().strftime('%d.%m.%Y')} {'*' * 5}")

    def log_to_txt(self, message: str, prettify: bool = True):
        """
        Записывает переданную строку в текстовый файл по пути, указанном при инициализации объекта класса

        :param message: строка, которая будет записана
        :param prettify: если истинно, строка запишется в виде "[ЧАС:МИНУТА:СЕКУНДА] строка" вместо "строка"
        :return: нет
        """
        datetime_mark = dt.today()
        with open(self.txtFilepath, 'a') as file:
            hour_minute_prefix = f"[{datetime_mark.strftime('%H:%M:%S')}] " if prettify else ''
            file.write(f"{hour_minute_prefix}{message}\n")

    def log_to_db(self, message: str):
        """
        Записывает переданную строку в базу данных по пути, указанном при инициализации объекта класса

        :param message: строка, которая будет записана
        :return: нет
        """
        datetime_mark = dt.today()
        with sqlite3.connect(self.dbFilepath) as db:
            db.execute('INSERT INTO logs (message, date_mark, time_mark) VALUES (?, ?, ?)',
                       (message, datetime_mark.strftime('%Y-%m-%d'), datetime_mark.strftime('%H:%M:%S'))
                       )
            db.commit()

    def full_log(self, message: str):
        """
        Записывает переданную строку в базу данных и в текстовый файл

        :param message: строка для записи
        :return: нет
        """
        self.log_to_db(message)
        self.log_to_txt(message)

    def select_last_x_messages_from_db(self, amount: int = 50):
        """
        Возвращает из базы данных последние сообщения в указанном количестве в порядке last-in-first-out

        :param amount: количество сообщений для возврата
        :return: генератор из полученных сообщений
        """
        with sqlite3.connect(self.dbFilepath) as db:
            msgs = db.execute('SELECT message FROM logs ORDER BY id DESC LIMIT ?', (amount,)).fetchall()
            return (item[0] for item in msgs[::-1])

