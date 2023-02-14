from time import sleep
from kettle import MiMak1
from input_modification import input_with_timeout

k = MiMak1()
def assure_input_is_int(inp):
    try:
        inp = int(inp)
    except (ValueError, TypeError):
        inp = 0
    finally:
        return inp


def main(text):
    k.logs.append(f'ТЕМПЕРАТУРА: {k.current_temperature}')
    print('\n' * 100)
    print(text)

    ans = assure_input_is_int(
            input_with_timeout(1)
          )

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

    new_text = k.generate_response()
    main(new_text)

print('\n' * 100)
print(f'Вас приветствует интерфейс взаимодействия с чайником {k}.\nДобро пожаловать!\n\n')
ans = assure_input_is_int(
        input('1. Включить чайник\n\nВведите команду:\n')
      )

match ans:
    case 1:
        k.switch_power()
        text = k.generate_response()
        while k.is_powered:
            main(text)
    case _:
        pass

print(f'\nСпасибо, что воспользовались {k}. Приятного чаепития!')
