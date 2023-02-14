from time import sleep
from kettle import MiMak1
from input_modification import input_with_timeout

k = MiMak1()


def main(text):
    print(text)

    ans = input_with_timeout(1)
    try:
        ans = int(ans)
    except (ValueError, TypeError):
        ans = 'Не удалось распознать команду'

    match ans:
        case 1:
            k.switch_status('power')
        case 2:
            k.switch_status('busy')
        case _:
            pass

    if k.status['busy']:
        k.boil()

    new_text = k.generate_response(ans)
    main(new_text)


print(f'Вас приветствует интерфейс взаимодействия с чайником {k}.\nДобро пожаловать!\n')

while k.status['power']:
    text = f"\n1. {'Включить' if k.status['power'] else 'Выключить'} чайник" \
           f"\n 2. {'Начать' if k.status['busy'] else 'Остановить'} кипячение" \
           f'Введите команду [1-2]:'
    main(text)