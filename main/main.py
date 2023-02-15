from kettle import MiMak1
from input_modification import input_with_timeout
from io_manager import CommandPanel


k = MiMak1()
cmd = CommandPanel()


# HELPER FUNCTIONS
def assure_input_is_num(inp, num_func):
    try:
        inp = num_func(inp)
    except (ValueError, TypeError):
        inp = 0
    finally:
        return inp


def main(interface_text, available_actions):
    print('\n' * 100)
    print(interface_text)

    if k.is_powered:
        k.logs.append(f"ТЕМПЕРАТУРА: {k.current_temperature if not k.is_empty() else 'вода не обнаружена'}")

        ans = input_with_timeout(1)

        if k.is_waiting_water:
            ans = assure_input_is_num(ans, float)
            k.add_water(ans)
            k.switch_waiting_water()

        else:
            ans = assure_input_is_num(ans, int)

            match ans:
                case 1:
                    k.switch_power()
                case 2:
                    k.switch_busy()
                case _:
                    pass

        if k.is_busy:
            k.boil()
        else:
            k.cool()

        ket_rep = k.generate_report()
        text, actions = cmd.generate_interface(ket_rep)
        main()


# MAIN WORKFLOW
print('\n' * 100)
text, actions = \
    cmd.generate_interface(k.generate_report(),
                           [
                               f'Вас приветствует интерфейс взаимодействия с чайником {k}. Добро пожаловать!\n',
                           ],
                           )
ans = input_with_timeout(1)

ans = assure_input_is_num(ans, int)
if ans in range(1, len(actions) + 1):
    actions[ans]()
match ans:
    case 1:
        k.switch_power()
        text, actions = cmd.generate_interface(k.generate_report())
        main(text)
    case _:
        pass

print(f'\nСпасибо, что воспользовались {k}. Приятного чаепития!')
