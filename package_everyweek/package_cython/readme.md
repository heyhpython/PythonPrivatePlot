## 1.compile cython code

### 1.1 Cython Compilation Pipeline
- cython cython代码的编译工作通过编译管道完成
- 编译管道分为两步
- 第一步由cython编译器将cython代码编译成平台自由c或c++  cython编译器实现
- 第二步将c或c++代码编译成对象文件`.o`，然后将对象文件链接成python扩展模块（linux/macos是.so的共享对象, windows是.pyd的动态库）pythonb标准库ditutils实现


```python
from distutils.core import setup
from Cython.Build import cythonize
setup(ext_modules=cythonize('fib.pyx'))
```
```bash
python setup.py build_ext --inplace
```
- `cythonize`方法将pyx文件转化为c文件,可以传入一个文件或文件序列或者文件名的规则，完成第一步
- `setup`方法将c文件转化为python扩展模块，即完成第二步
- `build_ext`参数让distuils编译`cythonize`生成的文件为扩展对象
- `--inplace`参数指定了生成文件的位置

### 1.1 run and compile by ipython

### 1.2 compile at import
```python
import pyximport
pyximport.install()
import fib 
```
- 此方法省去了新增setup.py的
- 当pyx文件修改之后，`pyximport`会自动识别并重新编译，在重新导入时生效
- 不建议在生产环境使用，因为cython依赖于适当的c编译器
- 在pyx文件相同目录增加同名的`.pyxdeps`文件，并列出pyx文件所依赖的c/c++或头文件等，`pyximport`会监控所有依赖文件的改动，并重新编译
```python
def make_ext(modname, pyxfilename):  # 必须
    from distutils.extension import Extension
    return Extension(modname, sources=[pyxfilename, '_fib.c'],include_dirs=["."])             
```
- 如若有外部以来（比如c），在pyx文件相同目录增加同名的`.pyxbld`文件
- 文件中定义`make_ext`函数指定模块名及pyx文件
- sources参数告知编译器用pyx文件c文件并进行链接
- include_dir参数告知disutils在当前目录查找头文件
### 1.3 compile separately by build tool
```bash
CFLAGS=${python-config --cflags}
LDFLAGS=${python-config --ldflags}
cython fib.pyx  # generate fib.c code
gcc -c fib.c ${CFLAGS} # generate fic.o with 
gcc fic.o -o fib.so -shared ${LDFLAGS}  # generate fic.so
```
- python-config--cflags 获取正确的编译flags 
- python-config --ldflags 获取正确的链接flags

### 1.4 integrated to build system for large project
```cmake
# Detects and activates Cython 
include(UseCython) 

# Specifies that Cython source files should generate C++ 
set_source_files_properties(
${CYTHON_CMAKE_EXAMPLE_SOURCE_DIR}/src/file.pyx 
PROPERTIES CYTHON_IS_CXX TRUE)

 # Adds and compiles Cython source into an extension module 
cython_add_module( modname file.pyx cpp_source.cxx)
```

```make
INCDIR := $(shell python -c \ 
"from distutils import sysconfig; print(sysconfig.get_python_inc())")

#To acquire the Python dynamic libraries to link against, we can use: 
LIBS := $(shell python -c \ 
        "from distutils import sysconfig; \ 
        print(sysconfig.get_config_var('LIBS'))")
```

## 2.深入了解Cython 
### 2.1类型声明cdef
```
cdef int i
cdef float j, k
cdef: 
    double l = 0.0 # 值类型
    long *a # 指针类型
    int arr[10] # 数组
    size_t len  # 类型别名
    tm time_struct  # 复合类型（结构体货集合）
    void (*f)(int, double)  # 韩素指针类型
```
- cython支持c范围内的所有类型申明
### 2.2类型断言
```
cimport cython

@cython.infer_types(True)
def more_infer():
    i = 1
    d = 2.0
    c = 3 + 4j
    r = i * d + c
    return r
```
- 不设置`infer_types`时，cython会保守的进行类型推断
- 比如i=1不会推断为c的long， 但是d会被推断为c的double类型
- 设置了`infer_types=True`后，会进行严格的类型推断，c会被推断为long类型
- `infer_types`可以设置为函数层级或者全局

```
cdef double golden_ratio
cdef doube *p_double
p_double = &golden_ratio
p_double[0] = 1.618
```
- cython里值类型的取址任然用`&`，但是指针类型的取值使用`[0]`这样的用法
- 原因是`*`以及`**`已经被python用来作为关键字参数和命名参数的语法级解包用法里
```
from cython cimport operator
print(operator.dereference(p_double))
```
- `operator.dereference`这种不常用的方法也可以用来取值
- 访问结构体的属性时，c使用`->`，cython使用`.`访问

```
cdef:
    list particles
    dict names_from_particles
    str pname
    set unique_particles
```
- 静态的声明python类型的变量时，python内置的内型都可以
- 其他使用c实现且cython有权限获取声明的，比如`NumPy arrays`
```
-1 % 5 # python结果为4 c结果为-1
1/0  # python会检查分母并抛出除0错误，c则没有
```
- 当进行加减乘时，动态类型的python对象会有python的语义，而静态类型的变量会有c的语义，比如精度溢出等
- python和c在对有符号的整型数除法和取余上有明显不一样的行为
- cython在取余和除法默认使用python的语义，即使定义的是是静态类型
- 可以全局或模块级别使用`cdivision`
- 或直接在注释里使用`cython: cdivision=True`
- 甚至可以在函数级别使用`@cython.cdivision(True)`装饰器
- 或在函数里使用上下文`with cython.cdivision(True):


### 2.2 函数
- cython同事支持python和c类型的函数

#### 2.2.1 使用def关键字的python函数
```
def py_fact(n):
    if n<=1:
        return 1
    return n * py_fact(n-1)
```
- 这种方式会有一定的效率提升，但不明显

```
def c_fact(long n):
    if n <= 1:
        return 1
    return n * c_fact(n-1)
```
- 参数与返回值类型都没静态的声明，节省了类型推断的时间
- 这种用法的时间消耗与纯c相近，通常用在尽可能类似c但是不写c代码时

#### 2.2.2 使用cdef关键字的c函数
```
cdef long c_fact(long n):
    if n <= 1:
        return 1
    return n * c_fact(n-1)
```
- cdef 的函数可以在同一个cython源码文件中被cdef或者def的函数调用，
- 但不能直接被外部导入或调用,可使用def的函数包一层来暴露cdef的函数

#### 2.2.3 混合cdef与def使用cpdef关键字的函数
```
cpdef inline long cp_fact(long n):
    if n <= 1:
        return 1
    return n * cp_fact(n-1)
```
- cpdef函数既有python函数的灵活方便，也有c函数的性能, 与c_fact相近
- cython的cdef和cpdef支持c和c++中的inline关键字，当正确地使用时，可以提高性能
- cpdef的函数的参数和返回值必须与python和c类型兼容，任何可以在c层级表现的Python对象都可以
- 但是不可不加选择的使用c的指针、数组作为参数和返回值

#### 2.2.4 异常处理
- def定义的函数在c的层级总是返回的python对象的指针,这可以使cython正确的从def函数中抛出错误
- cdef和cpdef函数返回的是非python类型
```
cpdef double divide_ints(int i, int j):
    return i / j
```
- 在cython以前的版本，这种情况下当除以0时会给出警告但是返回0，cython0.29.15中，已经是直接抛出错误了
```
cpdef double divide_ints(int i, int j) except? -1:
    return i / j
```
- 这种操作会抛出详细的错误调用栈
- `except? -1`使当返回值为-1时作为错误发生的标志让cython去检查全局错误的状态，并进行错误栈展开
- 若函数没有异常且返回值是-1，cython不会抛出异常
- `-1`可以时任意一个在返回值类型范围内的数

#### 2.2.5 类型转换
```
cdef void *v
cdef int *ptr_i = <int*>v 
```
- 将void *类型转化为了int *
- 当对要转化的类型不甚确定是可在类型后加问号`<int*?>v`, 当要转化的类型与需要的类型无法匹配时，抛出类型错误

### 2.3 声明和使用结构体、集合和枚举类型
```
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
```

## 3.cython里的循环语句
```
cdef int N
for i in range(N):
    ...
```
- 如果在循环体中不适用i，cython会将i自动设为int型
- 如果在循环体中使用i， cython无法确定是否会溢出，因此无法推断
- 如果确定不会精度溢出， 应该静态的声明i的类型
```
cdef int i, N
for i in range(N):
    ...
```
- 当遍历一个容器时，最好将容器转化成c++的容器会更高效
- 使用固定类型的变量以及cdef的函数会让循环更高效
- 内部有跳出循环语句的死循环可以被自动转化成高效的c代码

```python
# python 版本
a = [1, 2, 3, 4, 5]
n = len(a) - 1
for i in range(1, n):
    a[i] = (a[i-1] + a[i] + a[i+1])/3.0
```

```
# 高效的cython版本
a = [1, 2, 3, 4, 5]
cdef unsigned i, n = len(a) - 1
for i in range(1, n):
    a[i] = (a[i-1] + a[i] + a[i+1])/3.0
```

## 4.ptyhon类与cython扩展类型
```
cdef class Particle:
    """simple particle extension type
        class not define with cdef is a normal python class, not an extension type
    """
    cdef double mass, position, velocity

    def __init__(self, m, p, v):
        self.mass = m
        self.position = p
        self.velocity = v

    def get_momentum(self):
        return self.mass * self.velocity
```
- `cdef class`语句告诉cython创建一个扩展类型而不是正常的python类型
- 扩展类型的所有属性必须使用cdef静态申明
- cdef申明的属性无法在python中访问，无法动态添加属性
- 原因是扩展对象实例化的时候会创建并初始化一个c的结构体，这一步要求结构体的所有字段和大小都明确，因此需要用cdef什么属性

#### 4.1类型属性和访问控制
```
cdef class Particle:
    cdef readonly double mass, 
    cdef public double position, 
    cdef double velocity
    ...
```
- 默认情况下cdef的属性无法在python中访问
- 但加了关键字readonly后，可以在Python中访问，但无法修改
- 加了public的关键字的变量， 可以在python中访问并修改

#### 4.2 c层级的初始化和清除
```
cdef class Matrix:
    cdef:
        unsigned int nrows, ncols
        double *_matrix

    def __cinit__(self, nr, nc):
       self.nrows = nr
       self.ncols = nc
       self._matrix = <double*>malloc(nr*nc*sizeof(double))
       if self._matrix == NULL:
           raise MemoryError()
           
    def __dealloc__(self):
        if self._matrix != NULL:
            free(self._matrix)
```
- cython为了确保扩展类型的对象初始化前，储存属性的c结构体已经被创建，添加了__cinit__方法
- __cinit__方法会在__init__和__new__方法之前执行，并确保有且只有执行一次
- 若定义了__dealloc__方法，cython会确保在清除时调用一次该方法

#### 4.3cdef和cpdef的方法
- 不可用cdef或cpdef在非cdef的扩展类型里，会报编译错误
- cdef与cpdef方法的表现与函数类似，在python中无法访问cdef函数，可以访问cpdef
- cpdef函数被Python调用时会将返回值转化为python类型，应该返回值不可以时python不支持的类型，比如指针类型

#### 4.4扩展类型的继承和多态
```
cdef class InheirParticle(CyParticle):
    pass

```
- 扩展类型可以继承自一个用c实现的基础类型（内置类型或其他扩展类型），但不可以继承自python类或者继承多个
```
cdef Particle static_p = p
```
- 当p是动态类型对象时，cython不能访问任何c层级的数据或方法，而是要通过python/c api来查找，消耗很大
- 使用cython的casting 操作器，静态指定一个新的变量类型，并且赋值为p
- 如果p不是Particle类型实例，会抛出类型错误
- 再使用static_p的方法时，使用的就是Particle类型定义的方法，也可以访问p不可以访问的私有属性
- cython对动态类型对象使用通常的python方法查找，当方法是cdef定义时，会查找失败
- 为了保证对象有访问cdef方法的权限，必须要提供对象的静态类型声明
`(<Particle>p).velocity`
`(<Particle？>p).velocity`
- 使用casting操作器达到上述定义临时变量的效果
- 使用圆括号是因为c操作符的优先级问题
- 当p不是`Particle`类型时，会抛出语法错误，因此使用第二种类型检查的cast会更合适

#### 4.5扩展类型和None值
```
def dispatch(Particle p):
    print(p.get_momentum())
    print(p.velocity)
```
- 即便None不是`Particle`类型，cython也允许在此处传入None而不会有编译错误
- 但是在执行时，None值没有`Particle`类型的c api,因此会抛出语法错误
- 所以为了避免出现语法错误，在访问任何c层级的属性或方法时，应该先对空值进行校验
- cython提供了空值检查的编译指令，可以在文件头全局配置`cython: nonecheck=True`
- 或编译时指定`cython --directive nonecheck=True source.pyx 

#### 4.6扩展类型的property
```
cdef class Particle:
    ...
    property momentum:
        """定义python的momentum属性"""
        def __get__(self):
            return self.mass * self.velocity

        def __set__(self, m):
            self.velocity = m / self.mass
    
```

#### 4.7cython扩展类型的特殊方法（python魔法方法的cython版本）
- cython不支持__del__方法，替代者是__dealloc__

#### 4.7.1算数运算符重载
- 扩展类型不支持`__radd__`，仅以`__add__`充当add和radd的角色
```
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
```
- cython不会对`__add__`的两个参数进行类型推断，因此，为了访问data属性，需要进行类型cast
- `__add__`的两个参数代表的是想加的两边
- 其他的算术运算用法于此类似
- in_place操作比如`__iadd__`总是将类的实例作为第一个参数，因此可以使用正常的self作为第一个参数
- in-place操作的例外是`__ipow__`，他的用法与`__add__`一致

#### 4.7.2比较运算符
- cython不支持python中的`__eq__, __lt__, __le`等，
- 而是提供了`__richcmp__(x, y, op)`方法作为替代
- op参数接收一个整形数字，表明需要进行的比较方式,对照如下
```
from cpython.object cimport Py_LT, Py_LE, Py_EQ, Py_NE, Py_GT, Py_GE
Py_LT   < 
Py_LE   <= 
Py_EQ   == 
Py_NE   != 
Py_GT   > 
Py_GE   >=
```
- 这些整型数字是python编译时常亮，定义在python运行时object.h