# cython: language_level=3
#cython: profile=True


def py_integrate(a, b, f, N=2000):
    dx = (a-b)/N
    s = 0.0
    for i in range(N):
        s += f(a + i*dx)
    return s * dx

cimport cython

@cython.cdivision(True)
cdef double integrate(double a, double b, double(*f)(double), int N=2000):
    cdef:
        double dx = (a-b)/N
        double s = 0.0
        int i
    for i in range(N):
        s += f(a + i*dx)
    return s * dx


from libc.math cimport sin
cimport cython

# @cython.profile(True)
def sin2(x):
    return sin(x)**2