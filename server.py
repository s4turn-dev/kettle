from flask_app import app, k
from datetime import datetime as dt

if __name__ == '__main__':
    app.run()
    k.logger.log_to_txt(f"{'-' * 30} ЗАПУСК ОТ {dt.today().strftime('%d.%m.%Y')} {'-' * 30}", False)
    k.logger.log_to_db(f"{'*' * 5} ЗАПУСК ОТ {dt.today().strftime('%d.%m.%Y')} {'*' * 5}")
