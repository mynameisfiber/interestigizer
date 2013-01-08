#!/usr/bin/env python2.7

import numpy as np
import ctypes as ct

class Region(ct.Structure):
    _fields_ = [
        ("size_x", ct.c_int),
        ("size_y", ct.c_int),
        ("loc_x", ct.c_int),
        ("loc_y", ct.c_int),
    ]

_lib_largest_squareish = np.ctypeslib.load_library('largest_squareish', '.')

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

def _format_response(result_raw):
    result = {}
    for attribute in result_raw.contents._fields_:
        attr = attribute[0]
        result[attr] = getattr(result_raw.contents, attr)
    return result

def largest_squareish_matrix(mat, value=0):
    assert isinstance(mat, np.ndarray)

    rows, cols = mat.shape
    result_raw =  _lib_largest_squareish.largest_squareish_matrix(mat, rows, cols, value)
    return _format_response(result_raw)

def largest_squareish_histogram(hist, value=0):
    assert isinstance(hist, np.ndarray)

    rows, = hist.shape
    result_raw =  _lib_largest_squareish.largest_squareish_histogram(hist, rows, 0)
    return _format_response(result_raw)

