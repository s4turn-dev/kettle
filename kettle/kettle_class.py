from . import config
from logger import Logger


class BasicKettle:
    def __init__(self, name, version):
        self.model = name
        self.version = version

        self.logger = Logger(config.DB_FILEPATH, config.TXT_FILEPATH)
        
        # camelCase-нейминг, чтобы не путать is-методы с is-атрибутами
        self.isPowered = False
        self.isBusy = False
        self.isWaitingWater = False

        self.water_amount = 0
        self.current_temperature = config.TEMPERATURE_MIN
        self.boiling_time_left = config.SECONDS_TO_BOIL

    def __str__(self):
        return f'{self.model}-{self.version}'

    def is_full(self) -> bool:
        return True if self.water_amount == config.KETTLE_CAPACITY else False

    def is_empty(self) -> bool:
        return True if self.water_amount == 0 else False

# Переключатели состояний
    def switch_power(self):
        self.isPowered = not self.isPowered
        if self.isBusy:
            self.switch_busy()
        self.logger.full_log(f"ЧАЙНИК {'ВКЛЮЧЕН' if self.isPowered else 'ОТКЛЮЧЕН'}")

    def switch_busy(self):
        if not self.isPowered and not self.isBusy:
            self.logger.full_log('ОШИБКА: Чайник отключен. Включите, чтобы кипятить.')
        elif self.is_empty() and not self.isBusy:
            self.logger.full_log('ОШИБКА: Чайник пуст. Кипятить нечего. Налейте водички.')
        else:
            self.isBusy = not self.isBusy
            self.boiling_time_left = config.SECONDS_TO_BOIL
            self.logger.full_log(f"КИПЯЧЕНИЕ {'НАЧАТО' if self.isBusy else 'ОСТАНОВЛЕНО'}")

    def switch_waiting_water(self):
        self.isWaitingWater = not self.isWaitingWater
# ---------------

# Основной функционал
    def boil(self):
        if self.isPowered and self.isBusy:
            temperature_raising_step = round((config.TEMPERATURE_MAX - self.current_temperature) / self.boiling_time_left, 1)
            self.current_temperature += temperature_raising_step
            self.boiling_time_left -= 1

            if self.boiling_time_left == 0:
                self.switch_busy()
                self.logger.full_log('ЧАЙНИК ВСКИПЕЛ')

    def cool(self):
        self.current_temperature -= config.TEMPERATURE_COOLING_STEP
        if self.current_temperature < config.TEMPERATURE_MIN:
            self.current_temperature = config.TEMPERATURE_MIN

    def add_water(self, inserted_amount):
        # Чек на валидность количества воды
        if inserted_amount <= 0:
            pass
        else:
            # Чек на превышение вместимости
            if self.water_amount + inserted_amount > config.KETTLE_CAPACITY:
                self.logger.full_log(
                    f"В чайнике {'не было' if self.is_empty() else f'было {self.water_amount} л'} воды, "
                    f"и вы попытались влить {inserted_amount} л. "
                    "Теперь у вас есть полный чайник и лужа на полу.") 
                self.water_amount = config.KETTLE_CAPACITY
            # Вместимость не превышена и количество воды положительное
            else:
                self.water_amount += inserted_amount
                self.logger.full_log(
                    f'ВНЕСЕНИЕ ВОДЫ В ЧАЙНИК: {inserted_amount} л')  # Хахаха, надо обязательно оставить именно такую формулировку
# ---------------

    def generate_CLI_interface(self, optional_message: str | None = None) -> str:
        # Подтягиваем логи и склеиваем их в одну строку
        logs = self.logger.select_last_x_messages_from_db(config.LOG_LINES_AMOUNT_FOR_SCREEN)
        logs = '\n\n'.join(logs) 

        # Наводим красоту для сообщения
        optional_message = f'\n{optional_message}\n' if optional_message else None

        # Генеририуем панель информации
        info_panel = "СОСТОЯНИЕ ЧАЙНИКА\n\n" \
                     f"ВКЛЮЧЕН: {'Да' if self.isPowered else 'Нет'}\n" \
                     f"КИПЯТИТ: {'Да' if self.isBusy else 'Нет'}\n" \
                     f"ВОДА: {self.water_amount} / {config.KETTLE_CAPACITY} л" \
                     if config.SHOW_KETTLE_STATUS else None

        # Генерируем панель управления
        menu = f"1. {'Отключить' if self.isPowered else 'Включить'} чайник\n" \
               f"2. {'Остановить' if self.isBusy else 'Начать'} кипячение\n" \
                "3. Налить водички"
        input_prompt = 'Введите количество водички (число с плавающей точкой)' if self.isWaitingWater else 'Введите номер команды [1-3]'
        command_panel = f'{menu}\n\n{input_prompt}:'

        # Склеиваем все в одну строку
        interface = f"\n{'-' * 20}\n".join((item for item in (f'{logs}\n', optional_message, info_panel, command_panel) if item))
        return interface


class MiMak1(BasicKettle):
    def __init__(self):
        super().__init__('MiMak', 1)

    def switch_waiting_water(self):
        # Избегаем вычислений средней температуры воды
        if self.isBusy:
            self.logger.full_log(
                    f'ОШИБКА: Доливание водички в кипящий чайник не поддерживается в модели {self.model} версии {self.version}. '\
                     'Нам очень жаль. Извините.')
        else:
            self.isWaitingWater = not self.isWaitingWater
