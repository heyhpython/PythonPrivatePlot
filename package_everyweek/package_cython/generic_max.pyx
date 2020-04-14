cimport cython

ctypedef fused int_or_float:
    cython.short
    cython.int
    cython.long
    cython.float
    cython.double


cpdef int_or_float generic_max(int_or_float a,
                               int_or_float b):
    return a if a >= b else b

def my_max(a, b):
    return int_or_float(a, b)