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
        k.logs.append(f"ТЕМПЕРАТУРА: {k.current_temperature if not k.is_empty() else 'вода не обнаружена'}")
        ans = input_with_timeout(1)
    else:
        ans = input()

    # Решаем, что делать с вводом, в зависимости от того, ждет ли сейчас чайник воду
    if k.isWaitingWater:
        # "Наливаем" воду и перестаем ее ждать
        ans = assure_input_is_num(ans, float)
        k.add_water(ans)
        k.switch_waiting_water()
    else:
        # Действуем по выданной команде
        ans = assure_input_is_num(ans, int)
        match ans:
            case 1:
                if k.isPowered:
                    return
                else:
                    k.switch_power()
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
interface = k.generate_CLI_interface()
main(interface)

print('\nПриятного чаепития!')
