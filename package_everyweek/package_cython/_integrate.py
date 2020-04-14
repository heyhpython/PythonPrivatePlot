# coding=utf-8
# builtins
# third party package
# self built


def integrate(a, b, f, N=2000):
    dx = (a-b)/N
    s = 0.0
    for i in range(N):
        s += f(a + i*dx)
    return s * dx
