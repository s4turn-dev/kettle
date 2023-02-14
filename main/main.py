from signal import signal, SIGALRM, alarm
from time import sleep
from kettle import MiMak1

k = MiMak1()


def handler(signum, frame):
    print("Forever is over!")
    raise Exception("end of time")


def loop_forever():
    import time
    while 1:
        print("sec")
        time.sleep(1)


signal(SIGALRM, handler)
alarm(10)

print(f'Вас приветствует интерфейс взаимодействия с чайником {k}.\nДобро пожаловать!\n')

for x in range(5):
    try:
        loop_forever()
    except Exception as exc:
        print(exc)
        alarm(10)
