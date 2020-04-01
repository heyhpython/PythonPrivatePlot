# cython: language_level=3
ctypedef double real_t

cdef class State:
    cdef:
        public unsigned  int n_particles
        real_t *x
        real_t *vx

    cpdef real_t momentum(self)


cpdef run(State st)

cpdef int step(State st, real_t timestep)
