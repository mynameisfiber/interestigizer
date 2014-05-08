
import numpy

cimport numpy
cimport largest_squareish_cdefs

cdef class Region:
    cdef largest_squareish_cdefs.Region* _c_region
    cdef bint c_is_larger_than(self, largest_squareish_cdefs.Region* other):
        return largest_squareish_cdefs.is_larger(self._c_region, other)
    cdef bint c_is_larger_than_params(self, int start, int pos, int height):
        return largest_squareish_cdefs.is_larger_params(self._c_region, start, pos, height)

cdef void* c_largest_squareish_histogram(int *histogram, int N, int row):
    return largest_squareish_cdefs.largest_squareish_histogram(histogram, N, row)

cdef void* c_largest_squareish_matrix(double *histogram, int N, int M, double value):
    return largest_squareish_cdefs.largest_squareish_matrix(histogram, N, M, value)

def largest_squareish_histogram(numpy.ndarray[int, ndim=1, mode="c"] histogram not None, int row=0):
    cdef largest_squareish_cdefs.Region* out = <largest_squareish_cdefs.Region*>c_largest_squareish_histogram(<int*>histogram.data, histogram.shape[0], row)
    return dict(size_x=<int>out.size_x, size_y=<int>out.size_y, loc_x=<int>out.loc_x, loc_y=<int>out.loc_y)

def largest_squareish_matrix(numpy.ndarray[double, ndim=2, mode="c"] histogram not None, double value=0):
    cdef largest_squareish_cdefs.Region* out = <largest_squareish_cdefs.Region*>c_largest_squareish_matrix(<double*>histogram.data, <int>histogram.shape[0], <int>histogram.shape[1], value)
    return dict(size_x=<int>out.size_x, size_y=<int>out.size_y, loc_x=<int>out.loc_x, loc_y=<int>out.loc_y)

def solve_matrix(matrix_histo):
    return largest_squareish_matrix(numpy.asarray(matrix_histo, dtype=numpy.double))