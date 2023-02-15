from config import CAPACITY
from kettle import KettleReport


class CommandPanel:
    START_BOILING_VERB = 'Начать'
    STOP_BOILING_VERB = 'Остановить'
    TURN_KETTLE_ON_VERB = 'Включить'
    TURN_KETTLE_OFF_VERB = 'Отключить'
    KETTLE_NOUN = 'чайник'
    BOILING_NOUN = 'кипячение'

    FILL_KETTLE_COMMAND = 'Налить водички'

    WAITING_WATER_PROMPT = 'Введите количество воды (число с плавающей точкой от 0 до {})'
    WAITING_COMMAND_PROMPT = 'Введите номер команды [{}]'

    TEXT_DIVIDER = f"{'-' * 20}\n"

    def generate_interface(self, kr: KettleReport, optional_messages_list: list[str] | None = None):
        logs = '\n\n'.join(kr.logs)

        # Если чайник в состоянии ожидания водички, то подсказываем, что мы ждем не команду, а число вливаемой водички
        if kr.is_waiting_water:
            command_panel = f'\n{self.WAITING_WATER_PROMPT.format(CAPACITY - kr.water_amount)}'
            available_actions = None
        else:
            # Включение/отключение чайника — постоянно доступная опция вне зависимости от всего остального
            commands = [f"1. {self.TURN_KETTLE_OFF_VERB if kr.is_powered else self.TURN_KETTLE_ON_VERB} {self.KETTLE_NOUN}"]
            available_actions = {1: kr.actions['switch_power']}

            # Если чайник включен, то можно начать/остановить кипячение
            if kr.is_powered:
                commands.append(f"{len(commands) + 1}. {self.STOP_BOILING_VERB if kr.is_busy else self.START_BOILING_VERB} {self.BOILING_NOUN}")
                available_actions[len(commands)] = kr.actions['switch_power']

            # Если чайник сейчас не кипятит воду и он еще не полон, то можно налить водички
            if not kr.is_busy and not kr.water_amount == CAPACITY:
                commands.append(f"{len(commands)}. {self.FILL_KETTLE_COMMAND}")
                available_actions[len(commands)] = kr.actions['switch_waiting_water']

            # Мы не ждем водичку, поэтому подсказкой будет призыв ввести номер команды, а не число водички
            commands.append("\n"
                            f"{self.WAITING_COMMAND_PROMPT.format('1' if len(commands) == 1 else f'1-{len(commands)}')}"
                            )
            command_panel = '\n'.join(commands)

        # Переменная распаковывается как список парой строк ниже, поэтому нужно убедиться, что это список
        if optional_messages_list is None:
            optional_messages_list = []

        text = self.TEXT_DIVIDER.join([logs, *optional_messages_list, command_panel])
        return text, available_actions

