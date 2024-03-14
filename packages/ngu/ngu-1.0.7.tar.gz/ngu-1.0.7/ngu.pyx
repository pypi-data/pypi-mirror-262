cimport cython
from libcpp.string cimport string
from libcpp.vector cimport vector

cdef extern from "./ngu/ngu.h":
    cdef cppclass ABC:
        int a

cdef class PyABC:
    cdef ABC __CXX_object

    def __cinit__(self):
        pass
    

