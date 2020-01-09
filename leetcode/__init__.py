# coding=utf-8
# builtins
import time
# third party package
# self built


def timer(func):
    def warp(*args, **kwargs):
        s = time.time()
        ret = func(*args, **kwargs)
        print('eceute time: ', time.time() - s)
        return ret
    return warp