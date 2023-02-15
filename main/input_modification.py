# Привет, дорогой ревьюер! Я уже сказал в README, но на всякий случай хочу повториться:
# я не написал ни строчки кода в этом файле. Одновременные чтение ввода и постоянные выводы в консоль —
# проблема, с которой мне не приходилось ранее ни сталкиваться, ни тем более решать.
# Поэтому, поняв, что именно мне нужно для решения проблемы, я обратился в поисках ответа к интернету и
# подогнал то, что нашел, под необходимое по ТЗ поведение.
# Источик: https://gist.github.com/r0dn0r/d75b22a45f064b24e42585c4cc3a30a0

import threading
import queue
from select import select
from sys import stdin


def _wait_for_enter(channel: queue.Queue, timeout: int = None):
    (rlist, wlist, xlist) = select([stdin], [], [], timeout)

    if len(rlist):
        line = stdin.readline()
        channel.put(line)


def input_with_timeout(timeout):
    channel = queue.Queue()
    thread = threading.Thread(target=_wait_for_enter, args=(channel, timeout))

    # by setting this as a daemon thread, python won't wait for it to complete
    thread.daemon = True
    thread.start()

    try:
        response = channel.get(True, timeout)
        return response
    except queue.Empty:
        pass

    return None
