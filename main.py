from input_modification import input_with_timeout
from kettle import MiMak1

k = MiMak1()


# HELPER FUNCTIONS
def assure_input_is_num(inp, num_func):
    try:
        inp = num_func(inp)
    except (ValueError, TypeError):
        inp = 0
    finally:
        return inp


def main(interface_text):
    # Обновляем интерфейс консоли
    print('\n' * 100)
    print(interface_text)

    # Получаем команду (пользовательский ввод)
    if k.isPowered:
        k.logger.full_log(f"ТЕМПЕРАТУРА: {f'{k.current_temperature}°C' if not k.is_empty() else 'вода не обнаружена'}")
        # Поскольку по ТЗ необходимо ежесекундно сообщать температуру воды, когда чайник включен,
        # то и ввода бесконечно ждать нельзя, поэтому используем ввод с таймаутом
        ans = input_with_timeout(1)
    else:
        ans = input()

    # Решаем, что делать с вводом, в зависимости от того, ждет ли сейчас чайник воду
    if k.isWaitingWater:
        ans = assure_input_is_num(ans, float)

        if ans == 0:
            pass
        # "Наливаем" воду и перестаем ее ждать
        else:
            k.add_water(ans)
            k.switch_waiting_water()
    else:
        ans = assure_input_is_num(ans, int)

        # Действуем по выданной команде
        match ans:
            case 1:
                k.switch_power()
                # Лучшее, к чему я смог придти в своей реализации, соответствующее "закончить программу, если чайник выключается" из ТЗ
                if not k.isPowered:
                    return
            case 2:
                k.switch_busy()
            case 3:
                k.switch_waiting_water()
            case _:
                pass

    # Изменяем температуру воды
    if k.isBusy:
        k.boil()
    else:
        k.cool()

    new_interface = k.generate_CLI_interface()
    main(new_interface)


# MAIN WORKFLOW
interface = k.generate_CLI_interface(f'Вас приветствует интерфейс взаимодействия с электройчаником {k}. Добро пожаловать!')
main(interface)

print('\nПриятного чаепития!')
