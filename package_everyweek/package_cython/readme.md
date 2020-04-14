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
- 这些整型数字是python编译时常亮，定义在python运行时object.


#### 4.7.3 迭代器
```
cdef class I:
    cdef:
        list data
        int i
    def __init__(self):
        self.data = list(range(100))
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.i >= len(self.data):
            raise StopIteration
        ret = self.data[self.i]
        self.i += 1
        return ret
```
- 实现了`__iter__`和`__next__`方法，则实例可以是一个迭代器

## 5.组织cython代码
```
.pyx # cython implemention code
.pxd # cython 定义文件
.pxi # cython 包含文件
```

### 5.1 pyx与pxd
- 当需要共享c层级的结构体时，我们需要创建一个定义文件
- 定义文件只在编译时用到，因此只能在文件里添加c层级的声明，python层级的`def`禁止放在定义文件中
- 定义文件的文件名与实现文件相同，因此被cython视作同一个命名空间，因此在pxd与pyx中的声明变量不能重名
- 任何对其他c层级的cython模块可以访问的，都需要在定义文件中
- 包括:
```
# c 类型定义 ctypedef struct union enum
# 为外部c或者c++库的定义
# cdef 或者cpdef模块级别的函数
# cdef的扩展类型
# cdef的扩展类型属性
# cdef和cpdef的方法
# c层级的行内函数或方法
```
- 不可包括：
```
python函数或非行内函数或方法
python类
在if或def代码块外可执行的python代码
```
- 外部的实现文件可以通过`cimport`访问simulator中所有的c层级的构造体

### 5.2 cimprot 语句
```
from simulator cimport State, step, real_t
from simulator import setup as sim_setup
```
- `cimport`导入的发生在编译时。并在pxd文件中查找只能cimportable的定义
- `import`语句工作在python层级，并在运行时导入
- `cimport`与`import`语法一致
- `cimport`python层级的对象会导致编译错误， `import`c层级的对象会导致编译错误
- `cimport` 与 `import` 都可以导入扩展类型和`cpdef`定义的函数，更让推荐`cimport`
- `import` 扩展类型或者`cpdef`函数只有python层级的权限，并且`cpdef`函数是通过python的包装调用
```
cdef extern "mt19937ar.h":
    void init_genrand(unsigned long s)
    unsigned long genrand_int32()
```
- `pxd`文件可以包含`cdef extern`代码块,任何其他`pyx`文件都可以导入并直接  使用该定义文件中的函数
- 在cython的安装路径有c,c++,python,numpy的预定义文件，提供直接接入相关api

### 5.3 cython的`include`语句和include文件`pxi`

```
IF UNAME_SYSNAME == "Linux":
    include "linux.pxi"
ELIF UNAME_SYSNAME == "Darwin":
    include "darwin.pxi"
IF UNAME_SYSNAME == "Windows":
    include "windows.pxi"
```
- 同一个文件使用两次`include`会导致编译错误
- 每个不同的`pxi`文件是统一接口的不同平台实现
- 推荐使用`cimport`，在必须要源代码层级的导入时，才使用`include`


## 6.用cyhton包装c库

### 6.1 用cython声明外部c代码
```
cdef extern from "header_name":
    从头文件中的缩进声明
```
- cython解释器会在生成的源文件中加入一行`#include "header_name" `
- 类型、函数和其他的在代码块的都可以从cython访问
- cython会在编译时检测c的声明被使用类型正确的方式使用，否则会抛出编译错误
- cython不会自动的包装已定义的对象，我们需要写`def`,`cdef`,`cpdef`来调用外部块中定义的c函数等

### 6.2 声明外部的c函数和类型定义
- `extern`块里最常见的是从c头文件搬运过来的函数和类型定义，但必须要修改一些地方
- 将`typedef`改为`ctypedef`
- 删除不需要和不知此的关键字，比如`restrict`,`volatile`
- 确保函数返回类型和名字在同一行声明
- 删除行结束符分号
```
# 1.直接照搬
cdef extern from "header.h":
    void(*signal(void(*)(int)))(int)
# 1.可读性更高的办法
cdef extern from "header.h":
    ctypedef void(*void_int_fptr)(int)
    void_int_fptr signal(void_int_fptr)
```
- 两种方式效果一致，第二种定义的`void_int_fptr`并不在c的头文件中
- 使用`extern`时，最好给函数参数一个名字，尤其是当参数名有意义时，有助于理解函数的作用

### 6.3声明和包装c结构体、集合、枚举值
```
cdef extern from "header_name":
    struct struct_name:
        struct_members
    
    union struct_name:
        struct_members

    enums struct_name:
        struct_members
```
- 语法与在cython中定义对应类型一致
- 如果是类型定义的类型，则使用`ctyprdef`关键字
```
cdef extern from "header_name":
    ctypedef struct struct_alias:
        struct_members
```
- 如果不需要使用结构体内的某一字段，但是又必须要将其作为不透明类型使用，可以在字段块使用pass
- `const`关键字对于定义函数参数可以省略
```
cdef extern from "printer.h":
    void _print "print"(fmt_str, arg)
```
- 可以给函数、结构体或类型定义一个别名，比如上例中在cython中使用`_print`来调用c的`print`函数
- 别名可以避免与python内置的函数或者关键字冲突

## 7.用cyhton包装c++库
- cython只能封装c++的公共方法和成员
```
cdef extern from "mt19937.h" namespace "mtrandom":
    unsigned int N
    cdef cppcclass MT_RNG:
        MT_RNG(undigned long s)
        MT_RNG(undigned long init_key[], int key_length)
        void init_genrand(unsigned long s)
        unsigned long genrand_int32()
        double genrand_real1()
```
- 使用cython`namespace`语句声明c++的namespace
- 使用`cppclass` 关键字声明c++的class
- 若没有命名空间，可以省去`namespace`语句
- 若有层级的命名空间。可以使用`ns_outer::ns_inner`
- 在`cppclass`代码块下声明c++ class的接口

### 7.1 包装扩展类型供python使用
```
cdef class RNG:
    cdef MT_RNG *_thisptr
    cdef __cinit__(self, unsigned long s):
        self._thisptr = new MT_RNG(s)
    cdef __dealloc(self):
        if self._thisptr != NULL:
            del self._thisptr 
    
    cpdef unsigned long randint(self):
        return self._thisptr.genranbd_int32()
    
    cpdef double rand(self):
        return self._thisptr.genranbd_real1()
    
```
- 使用`cpdef`函数封装c++方法

### 7.2 和c++代码一起编译
- 当编译c++项目时， 需要指定包含所有的c++源文件并且指定语言参数或指令
```python
from distutils.core import setup, Extension
from Cython.Build import cythonize

ext = Extension("RNG",sources=["RNG.pyx", "mt19937.cpp"], language="c++")   
setup(name="RNG", ext_modules=cythonize(ext))            
```
- 或者在`RNG.pyx`文件头指定 `distutils: language = c++` 和`distutils: sources=mt19937.cpp`
- 也可以使用`pyximport`编译扩展模块。但需要创建一个`RNG.pyxbld`文件，告诉pyximprot正在编译c++扩展，并且指明需要包含的c++源文件


### 7.3 重载函数和方法

#### 7.3.1通过参数分发
```
cdef class RNG:
    cdef MT_RNG *_thisptr
    cdef __cinit__(self, unsigned long s):
        if isinstance(s, int)：
            self._thisptr = new MT_RNG(s)   
        else：
            from cython.array cimport array
            arr = array("L", s)
            self._thisptr = new MT_RNG(arr.as_ulongs, len(arr)) 
```
- `重载` 根据不同的参数，执行同一个函数名的不同的函数体
- python不支持函数方法重载，因为我们需要根据不同的参数来调用不同的函数

#### 7.3.2通过`overloading`操作器

### 7.4c++的错误机制
- cython自动检测并转化c++的异常成python的异常，但是无法在`try catch`代码里捕获，也不可以在cython里抛出c++异常
- 为了捕获c++异常，在函数或方法的声明后加`except +`
- 为捕捉特定的错误，可以在`except +`后加特定的错误类型或者`cdef`函数的handler

```
cdef int handler():
    ...

cdef extern from "mt19937.h" namespace "mtrandom":
    unsigned int N
    cdef cppcclass MT_RNG:
        MT_RNG(undigned long s) except +
        MT_RNG(undigned long init_key[], int key_length) except +handler
```
### 7.5 c++类的继承
- cython的`cppclass`没有继承机制，因此在导入c++的子类和父类时，需要完全声明你需要的属性和方法
- 同一方法在基类和子类中的不同实现，再导入基类子类时，如果都申明了该方法，cython会对不同的类，生成正确的代码
- 或者显示的将子类型指针转换成基类，也可以访问基类实现的方法

### 7.6 模板函数和cython的混合类型
### 7.6 模板函数和cython的混合类型
```c++
template <class T>
const T& min(const T& a, const T& b);

template <class T>
const T& min(const T& a, const T& b);
```

```
cdef extern from "<algorithm>" namespace "std":
    const T max[T](T a, T b) except +
    const T min[T](T a, T b) except +
```
- 为了表明是模板函数，在函数名之后函数参数列表之前， 加上了方括号加上模板参数名`[T]`

### 7.7 模板类
```
cdef extern from "<vector>" namespace "std":
    cdef cppclass vector[t]:
        ...
```

## 8 cython 优化工具

### 8.1 运行时cprofile与cython的profile指令
```
import cProfile
cProfile.run("main()", sort="time")
```
- python内置的profile和cprofile可以调试python代码，但是不可以跨语言调试c代码。所有c代码的执行细节会丢失
- cython里定义的函数对于python的性能调试工具来说是一个黑箱，但是可以设置全局编译指令`# cython: profile=True`来支持运行时的性能分析
- cython支持对某一函数有选择性的调试
```
@cython.profile(True)
def sin2(x):
    ...
```
- 使用c标准包里的函数，比使用python的c接口要快

### 8.2 编译时性能分析和提示
- cython代码调用越少的python C API，那么性能就越好，因为调用c api需要在c对象和python 对象中转化，并且需要管理引用计数和错误处理等
- cython的编译器提供可选的表示`--annotate`或`-a` 告知cython生成代表cython源代码的网页文件`cython xx.pyx -a`
- 网页文件用不同的颜色区分调用python/c api的次数，调用次数越多越黑黄，越少越明黄，点击每一行可以看见生成的c代码

## 9.Numpy 和 `memoryview`

### 9.1 新的缓冲协议
- 是一个c层级的协议，python的对象可以实现协议
- 协议支持所有的python3版本
- 协议定义了一个c层级的结构体，有数据缓冲及数据层级、类型、读写权限的元数据
- 数据缓冲可以让使用者从不同的方式访问同一份数据，任何修改都是在原始数据上做修改，省略了数据的拷贝
- 支持的数据类型又`numpy ndarray`,python2的内置字符串类型，但是python2的unicode和python3的字符串类型不支持
- 内置的`bytearray`, 标准库的`array.array`和`ctypes.arrays`以及其他第三方类型，比如pil的多种图片类型

### 9.2 python的`memoryview`
- 是c层级缓冲的python代表，传入一个实现了协议的python对象可以创建一个`memoryview`对象
```python
bb = b'qeqweqwweq'
memv = memoryview(bb)
memv[0]
```
- 可以像访问列表一样去访问`memoryview`
- 但是是否可以修改数据则取决于原始数据的写权限
- 使用`memoryview`修改后，原始数据也会被修改

### 9.3 cython的`memoryview`
- cython的`memoryview`与python类时，但是更快
```
def summer(double[:] mv):
    cdef double d, ss = 0.0
    for d in mv:
        ss += d
    return ss
```
- `double[:] mv`定义mv一维为`typed momoryview`类型, 多维:`double[:,:,:]`
- 可以向访问列表一样访问mv的元素
- 在每次访问mv时，cython都会检查索引是否越界以及负数索引，会导致循环变慢
```
from cython cimport boundscheck, wraparound

with boundscheck(False), wraparound(False):
     ...
# 或者
@boundscheck(False)
@wraparound(False)
def xxxx:
    ...
# 或者
# cython: boundscheck=False
# cython: wraparound=False
```
- 当确定不会索引越界也不会使用负数时，可以使用如上方法关掉检查
```
cdef int a[3][5][7]
cdef int[:,:,::1] mv = a
```
- 可以直接将固定大小c的数组赋值给memoryview类型，因为固定大小的c数组总是内存连续的
```
from libc.stdlib cimport malloc 

def dynamic(size_t N, size_t M): 
    cdef long *arr = <long*>malloc(N * M * sizeof(long))
    cdef long[:,::1] mv = <long[:N, :M]>arr  # 会抛出错误
```
- 动态生成的数组也可以作为内存试图使用，但需要手动处理索引计算,不建议这样做
