# cython: language_level=3
def py_fact(n):
    if n<=1:
        return 1
    return n * py_fact(n-1)


def typed_fact(long n):
    if n<=1:
        return 1
    return n * typed_fact(n-1)


cdef long c_fact(long n):
    if n<=1:
        return 1
    return n * c_fact(n-1)

cpdef long cp_fact(long n):
    if n <= 1:
        return 1
    return n * cp_fact(n-1)
