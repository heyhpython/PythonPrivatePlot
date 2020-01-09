import time


def timer(func):
    def clock(*args, **kwargs):
        s = time.time()
        res = func(*args, **kwargs)
        print(time.time() - s)
        return res
    return clock
