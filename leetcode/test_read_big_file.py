# coding=utf-8
# builtins
from threading import Thread
import os
# third party package
# self built


def read_file(file_path, offset, limit):
    with open(file_path, 'r') as f:
        try:
            f.seek(offset)
            data = f.read(limit)
        except Exception as e:
            print(e)
            return
        print(data, end='/')


file_path = './__init__.py'
limit = 8
fils_size = os.path.getsize(file_path)

thread_count = fils_size // limit if fils_size % limit == 0 else fils_size // limit + 1


for i in range(thread_count):
    t = Thread(target=read_file, args=(file_path, i*limit, limit))
    t.start()
    t.join()