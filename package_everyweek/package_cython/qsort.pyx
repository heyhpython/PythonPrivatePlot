# cython: language_level=3

cdef extern from "stdlib.h":
    void *malloc(size_t size)
    void free(void *ptr)

cdef object py_cmp = None
ctypedef int (*qsort_cmp)(const void *, const void *) except *


cdef extern from "stdlib.h":
    void qsort(void *array, size_t count, size_t size,
               int (*compare)(const void *, const void *)except *) except *


def pyqsort(list x, reverse=False, comp_func=None):
    global py_cmp
    cdef:
        int *array
        int i, N
        qsort_cmp cmp_callback

    N = len(x)
    array = <int*>malloc(sizeof(int) * N)
    if array == NULL:
        raise MemoryError()

    for i in range(N):
        array[i] = x[i]
    if comp_func:
        py_cmp = comp_func
        if reverse:
            cmp_callback = r_py_cmp_wrapper
        else:
            cmp_callback = py_cmp_wrapper
    else:
        if reverse:
            cmp_callback = reverse_int_compare
        else:
            cmp_callback = int_compare

    qsort(<void*>array, <size_t>N, sizeof(int), cmp_callback )

    for i in range(N):
        x[i] = array[i]

    free(array)


cdef int int_compare(const void *a, const void *b) except *:
    cdef int ia, ib
    ia = (<int*>a)[0]
    ib = (<int*>b)[0]
    return ia - ib


cdef int reverse_int_compare(const void *a, const void *b)except *:
    return -int_compare(a, b)


cdef int py_cmp_wrapper(const void *a, const void *b)except *:
    cdef ia, ib
    ia = (<int*>a)[0]
    ib = (<int*>b)[0]
    return py_cmp(ia, ib)

cdef int r_py_cmp_wrapper(const void *a, const void *b)except *:
    return -py_cmp_wrapper(a, b)