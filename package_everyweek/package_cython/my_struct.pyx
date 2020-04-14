# cython: language_level=3
#1.1 定义虚数和集合结构体
cdef struct mycpx1:
    float real
    float imag

cdef union uu1:
    int a
    short b, c

#1.2定义类型别名
ctypedef struct mycpx:
    float real
    float imag

ctypedef union uu:
    int a
    short b, c
##1.3声明别名结构体类型的变量
cdef mycpx aa

#2初始化和使用结构体
##2.1初始化
## 2.1.1位置参数初始化
cdef mycpx a = mycpx(3.14, -1.0)
## 2.1.2关键字参数初始化
cdef mycpx b = mycpx(real=2.718, imag=1.618)
## 2.1.3赋值初始化
cdef mycpx zz
zz.real = 1
zz.imag = -1
## 2.1.4字典初始化
cdef mycpx xx = {'real':1.0, 'imag':-1.0}

# 3.定义枚举类型
cdef enum PRIMARIES:
    RED = 1
    YELLOW = 2
    BLUE = 3

cdef enum SECONDARIES:
    ORANGE, GREEN, PURPLE
# 也可以像struct或union使用ctypedef来声明枚举类型