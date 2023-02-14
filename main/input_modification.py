import threading
import queue
from select import select
from sys import stdin
import time


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


if __name__ == "__main__":
    while True:
        print(input_with_timeout(5))
