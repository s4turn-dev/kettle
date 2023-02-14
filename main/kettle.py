from datetime import datetime as dt
from typing_extensions import Literal


class BasicKettle:
    seconds_to_boil = 10
    maximum_temperature = 100.0
    starting_temperature = 20.0

    # Dunders
    def __init__(self, name, version):
        self.model = name
        self.version = version

        self.status = {'power': True, 'busy': False}
        self.current_temperature = self.starting_temperature

        self.temperature_history = []

    def __str__(self):
        return f'{self.model}-{self.version}'
    # ---------------

    # Info Helpers
    def is_on(self) -> bool:
        return self.status['power']

    def is_busy(self) -> bool:
        return self.status['busy']
    # ---------------

    # Main Functionality
    def switch_status(self, key: Literal['power', 'busy']):
        self.status[key] = not self.status[key]

    def boil(self):
        self.current_temperature += round((self.maximum_temperature - self.current_temperature) / self.seconds_to_boil,
                                          1)
        self.seconds_to_boil -= 1

    # ---------------

    # User
    def generate_response(self, last_command: Literal[1, 2, 'Не удалось распознать команду']):
        text = ''

        for number in self.temperature_history:
            text += f'ТЕМПЕРАТУРА: {number}\n\n'

        text += f'\n--------------------Предыдущая команда: {last_command}' \
                f'\n' \
                f"\n1. {'Включить' if self.status['power'] else 'Выключить'} чайник" \
                f"\n 2. {'Начать' if self.status['busy'] else 'Остановить'} кипячение" \
                f'Введите команду [1-2]:'

        return text
    # ---------------


class MiMak1(BasicKettle):
    def __init__(self):
        super().__init__('MiMak', 1)
