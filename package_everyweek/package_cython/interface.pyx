# cython: language_level=3

IF UNAME_SYSNAME == "Linux":
    include "linux.pxi"
ELIF UNAME_SYSNAME == "Darwin":
    include "darwin.pxi"
IF UNAME_SYSNAME == "Windows":
    include "windows.pxi"