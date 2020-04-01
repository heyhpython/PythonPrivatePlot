# coding=utf-8
# builtins
from distutils.core import setup
from Cython.Build import cythonize
# third party package
# self built
import os
cwd = os.path.dirname(__file__)
setup(ext_modules=cythonize('memo.pyx'))