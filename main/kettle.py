from datetime import datetime as dt
from typing_extensions import Literal


class BasicKettle:
    seconds_to_boil = 10
    max_temperature = 100.0
    min_temperature = 20.0
    temperature_cooling_step = 5.0

    # Dunders
    def __init__(self, name, version):
        self.model = name
        self.version = version

        self.is_powered = False
        self.is_busy = False
        self.current_temperature = self.min_temperature

        self.logs = []
        self.boiling_time_left = self.seconds_to_boil

    def __str__(self):
        return f'{self.model}-{self.version}'
    # ---------------

    # Main Functionality
    def switch_power(self):
        self.is_powered = not self.is_powered
        self.logs.append(f"ЧАЙНИК {'ВКЛЮЧЕН' if self.is_powered else 'ОТКЛЮЧЕН'}")

    def switch_busy(self):
        self.is_busy = not self.is_busy
        self.boling_time_left = self.seconds_to_boil
        self.logs.append(f'{self.boiling_time_left, self.seconds_to_boil}')
        self.logs.append(f"КИПЯЧЕНИЕ {'НАЧАТО' if self.is_busy else 'ОСТАНОВЛЕНО'}")

    def boil(self):      
        self.current_temperature += round((self.max_temperature - self.current_temperature) / self.boiling_time_left, 1)
        self.boiling_time_left -= 1
        if self.boiling_time_left == 0:
            self.switch_busy()
            self.logs.append('ЧАЙНИК ВСКИПЕЛ')
    
    def cool(self):
        self.current_temperature -= self.temperature_cooling_step
        if self.current_temperature < self.min_temperature:
            self.current_temperature = self.min_temperature
    # ---------------

    # User
    def generate_response(self):
        logs_text = '\n\n'.join(self.logs)
        command_panel = f"1. {'Отключить' if self.is_powered else 'Включить'} чайник\n" \
                        f"2. {'Остановить' if self.is_busy else 'Начать'} кипячение\n" \
                        f"\n" \
                        f"Введите команду [1-2]:"
        text = f'{logs_text}\n' \
               '--------------------\n' \
               f'{command_panel}'

        return text
    # ---------------


class MiMak1(BasicKettle):
    def __init__(self):
        super().__init__('MiMak', 1)
