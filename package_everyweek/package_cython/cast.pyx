# cython: language_level=3

def print_addr(a):
    cdef void *v = <void*>a
    cdef long addr = <long>v

    print("cython addr:", addr)
    print("python id:", id(a))