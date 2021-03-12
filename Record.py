import threading

import Config

lock = threading.Lock()
index = 0


def get_name():
    global index
    global lock

    lock.acquire()
    index = index + 1
    lock.release()

    name = Config.record + str(index)

    return name
