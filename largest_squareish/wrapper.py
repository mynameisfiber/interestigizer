#!/usr/bin/env python2.7

import numpy as np
import ctypes as ct
import os

CWD = os.path.dirname(__file__)

class Region(ct.Structure):
    _fields_ = [
        ("size_x", ct.c_int),
        ("size_y", ct.c_int),
        ("loc_x", ct.c_int),
        ("loc_y", ct.c_int),
    ]
    _b_needsfree_ = True

    def to_python(self):
        return {
            "size" : (self.size_x, self.size_y),
            "location" : (self.loc_x, self.loc_y),
        }

_lib_largest_squareish = np.ctypeslib.load_library('largest_squareish', CWD)

_lib_largest_squareish.largest_squareish_matrix.argtypes = [
    np.ctypeslib.ndpointer(dtype = np.double),
    ct.c_int,
    ct.c_int,
    ct.c_double,
]
_lib_largest_squareish.largest_squareish_matrix.restype = ct.POINTER(Region)

_lib_largest_squareish.largest_squareish_histogram.argtypes = [
    np.ctypeslib.ndpointer(dtype = np.intc),
    ct.c_int,
    ct.c_int,
]
_lib_largest_squareish.largest_squareish_histogram.restype = ct.POINTER(Region)

_lib_largest_squareish.largest_squareish_set_test.argtypes = [
    ct.c_int,
]
_lib_largest_squareish.largest_squareish_histogram.restype = ct.c_int

def set_test(val):
     return _lib_largest_squareish.largest_squareish_set_test(val)

def solve_matrix(mat, value=0):
    tmp = np.asarray(mat, dtype=np.double)
    rows, cols = tmp.shape
    result_raw =  _lib_largest_squareish.largest_squareish_matrix(tmp, rows, cols, value)
    return result_raw.contents.to_python()

def solve_histogram(hist, value=0):
    tmp = np.asarray(hist, dtype=np.intc)
    rows, = tmp.shape
    result_raw =  _lib_largest_squareish.largest_squareish_histogram(tmp, rows, 0)
    return result_raw.contents.to_python()

