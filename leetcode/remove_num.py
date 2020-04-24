# coding=utf-8
# builtins
from queue import Queue
# third party package
# self built


def main():
    q = Queue()
    # while 1:
    #     n = input()
    #     if n == '':
    #         break
    #     n = int(n)
    #     q.put(n)
    for j in range(8):
        q.put(j)
    i = 0
    while 1:
        if q.qsize() == 1:
            return q.get()
        n = q.get()
        if (i + 1) % 3 != 0:
            q.put(n)
        else:
            print(f"i:{i}, n:{n}")
        i += 1


import sys

