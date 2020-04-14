# cython: language_level=3


cdef class State:

    def __cinit__(self):
        self.n_particles = 10

    def __dealloc__(self):
        pass

    cpdef real_t momentum(self):
        pass


def setup(input_filename):
    pass


cpdef run(State st):
    pass


cpdef int step(State st, real_t timestep):
    pass


def output(State st):
    pass