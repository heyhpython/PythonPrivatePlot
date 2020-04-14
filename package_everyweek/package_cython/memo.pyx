# cython: language_level=3


def  summer1(double[:,] mv):
    cdef double d, ss = 0.0
    for d in mv:
        ss += d
    return ss


from cython cimport boundscheck, wraparound

def  summer2(double[:] mv):
    cdef double ss = 0.0
    cdef int  i, N
    with boundscheck(False), wraparound(False):
        N = mv.shape[0]
        for i in range(N):
            ss += mv[i]
        return ss