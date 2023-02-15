import config


# Создан для того, чтобы передавать состояние чайника I/O менеджеру
class KettleReport:
    def __init__(self, is_powered: bool, is_busy: bool, is_waiting_water: bool, logs: list, water_amount: float, actions: dict):
        self.is_powered = is_powered
        self.is_busy = is_busy
        self.is_waiting_water = is_waiting_water

        self.logs = logs
        self.water_amount = water_amount

        self.actions = actions


class BasicKettle:
    def __init__(self, name, version):
        self.model = name
        self.version = version
        self.logs = []

        self.is_powered = False
        self.is_busy = False
        self.is_waiting_water = False

        self.water_amount = 0
        self.current_temperature = config.TEMPERATURE_MIN
        self.boiling_time_left = config.SECONDS_TO_BOIL

    def __str__(self):
        return f'{self.model}-{self.version}'

    # Info Helpers
    def is_full(self):
        return True if self.water_amount == config.CAPACITY else False

    def is_empty(self):
        return True if self.water_amount == 0 else False
    # ---------------

    # Main Functionality
    def switch_power(self):
        self.is_powered = not self.is_powered
        self.logs.append(f"ЧАЙНИК {'ВКЛЮЧЕН' if self.is_powered else 'ОТКЛЮЧЕН'}")

    def switch_busy(self):
        if self.is_empty():
            self.logs.append('ОШИБКА: Чайник пуст. Кипятить нечего. Налейте водички.')
        else:
            self.is_busy = not self.is_busy
            self.boiling_time_left = config.SECONDS_TO_BOIL
            self.logs.append(f"КИПЯЧЕНИЕ {'НАЧАТО' if self.is_busy else 'ОСТАНОВЛЕНО'}")

    def switch_waiting_water(self):
        self.is_waiting_water = not self.is_waiting_water

    def boil(self):
        temperature_raising_step = round((config.TEMPERATURE_MAX - self.current_temperature) / self.boiling_time_left, 1)
        self.current_temperature += temperature_raising_step
        self.boiling_time_left -= 1

        if self.boiling_time_left == 0:
            self.switch_busy()
            self.logs.append('ЧАЙНИК ВСКИПЕЛ')
    
    def cool(self):
        self.current_temperature -= config.TEMPERATURE_COOLING_STEP
        if self.current_temperature < config.TEMPERATURE_MIN:
            self.current_temperature = config.TEMPERATURE_MIN

    def add_water(self, amount):
        if self.water_amount + amount > config.CAPACITY:
            self.water_amount = config.CAPACITY
            self.logs.append(f"В чайнике {'не было' if self.water_amount == 0 else f'было {self.water_amount} л'} воды,"
                             f"и вы попытались влить {amount} л.\n"
                             'Теперь у вас есть полный чайник и лужа на полу.')
        elif amount <= 0:
            pass
        else:
            self.water_amount += amount
            self.logs.append(F'ВНЕСЕНИЕ ВОДЫ В ЧАЙНИК: {amount} л')  # Хахаха, надо обязательно оставить именно такую формулировку
    # ---------------

    # User
    def generate_report(self):
        actions_kettle_capable_of = {
            'switch_power': self.switch_power,
            'switch_busy': self.switch_busy,
            'switch_waiting_water': self.switch_waiting_water,
        }

        report = KettleReport(self.is_powered,
                              self.is_busy,
                              self.is_waiting_water,
                              self.logs,
                              self.water_amount,
                              actions_kettle_capable_of
                              )
        return report
    # ---------------


class MiMak1(BasicKettle):
    def __init__(self):
        super().__init__('MiMak', 1)
