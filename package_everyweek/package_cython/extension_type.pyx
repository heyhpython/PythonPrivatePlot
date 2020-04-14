# cython: language_level=3


cdef class CyParticle:
    """simple particle extension type
        class not define with cdef is a normal python class, not an extension type
    """
    cdef readonly double mass
    cdef public double position
    cdef double velocity

    def __init__(self, m, p, v):
        self.mass = m
        self.position = p
        self.velocity = v

    cdef double get_momentum(self):
        return self.mass * self.velocity


class PyParticle:
    """simple particle extension type
        class not define with cdef is a normal python class, not an extension type
    """
    # cdef double mass, position, velocity

    def __init__(self, m, p, v):
        self.mass = m
        self.position = p
        self.velocity = v

    def get_momentum(self):
        return self.mass * self.velocity


cdef class CpyParticle:
    """simple particle extension type
        class not define with cdef is a normal python class, not an extension type
    """
    cdef readonly double mass
    cdef public double position
    cdef double velocity

    def __init__(self, m, p, v):
        self.mass = m
        self.position = p
        self.velocity = v

    cpdef double get_momentum(self):
        return self.mass * self.velocity

    @property
    def mass_(self):
        return self.mass


def add_momentum(pas):
    total_mom = 0.0
    for pa in pas:
        total_mom += pa.get_momentum()
    return total_mom

def add_momentum_c(list pas):
    # fastest way then
    cdef:
        double total_mom
        CyParticle pa
    for pa in pas:
        total_mom += pa.get_momentum()
    return total_mom


cdef class CPropertyParticle:
    """simple particle extension type
        class not define with cdef is a normal python class, not an extension type
    """
    cdef public double mass, velocity, position

    def __init__(self, m, p, v):
        self.mass = m
        self.position = p
        self.velocity = v

    property momentum:
        """定义python的momentum属性"""
        def __get__(self):
            return self.mass * self.velocity

        def __set__(self, m):
            self.velocity = m / self.mass


from cpython.object cimport Py_LT, Py_LE, Py_EQ, Py_NE, Py_GT, Py_GE


cdef class E:
    cdef int data

    def __init__(self, d):
        self.data = d

    def __add__(x, y):
        if isinstance(x, E):
            if isinstance(y, int):
                return (<E>x).data + y
        elif isinstance(y, E):
            if isinstance(x, int):
                return (<E>y).data + x
        else:
            return NotImplemented

    def __richcmp__(x, y, op):
        cdef:
            E e
            double data
        e, y = (x, y )if isinstance(x, E) else (y, x)
        data = e.data
        if op == Py_LT:
            return data < y
        elif op == Py_LE:
            return data <= y
        elif op == Py_EQ:
            return data == y
        elif op == Py_NE:
            return data != y
        elif op == Py_GT:
            return data > y
        elif op == Py_GE:
            return data >= y
        else: assert False

