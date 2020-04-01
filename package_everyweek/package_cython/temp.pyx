# cython: language_level=3
# distutils: language=c++
from libcpp.vector cimport vector


def get_v():
    cdef vector[int] *vec_int = new vector[int](10)
    print(1)
