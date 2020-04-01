# coding=utf-8
# builtins
import pyximport
pyximport.install()
from math import sin, pi
# third party package
# self built
# from package_everyweek.package_cython._integrate import integrate
from package_everyweek.package_cython.integrate import integrate, sin2


# def sin2(x):
#     return sin(x)**2


def main():
    a, b = 0.0, 2.0*pi
    return integrate(a, b, sin2, N=400000)


if __name__ == "__main__":
    import cProfile
    cProfile.run("main()", sort="time")