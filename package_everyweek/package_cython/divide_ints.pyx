# cython: language_level=3
# cython: embedsignature=True


cpdef double divide_ints(int i, int j) except? -1:
    return i / j