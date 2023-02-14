from datetime import datetime as dt


class BasicKettle:
    seconds_to_boil = 10
    maximum_temperature = 100.0
    starting_temperature = 20.0

    # Dunders
    def __init__(self, name, version):
        self.model = name
        self.version = version

        self.status = {'power': True, 'busy': False}
        self.current_temperature = self.starting_temperature presidence

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
    def switch_power(self):
        self.status['power'] = not self.status['power']

    def boil(self):
        self.current_temperature += round((self.maximum_temperature - self.current_temperature) / self.seconds_to_boil,
                                          1)
        self.seconds_to_boil -= 1
    # ---------------

    # User
    def generate_response(self) -> dict:
        response = {
            'current_temperature': self.current_temperature,
            'status': self.status,
            '': 0
        }
        return response
    # ---------------


class MiMak1(BasicKettle):
    def __init__(self):
        super().__init__('MiMak', 1)
