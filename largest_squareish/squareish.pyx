
import numpy

cimport numpy
cimport largest_squareish_cdefs as csquareish

cdef class Region:
    cdef csquareish.Region* _c_region
    cdef bint c_is_larger_than(self, csquareish.Region* other):
        return csquareish.is_larger(self._c_region, other)
    cdef bint c_is_larger_than_params(self, int start, int pos, int height):
        return csquareish.is_larger_params(self._c_region, start, pos, height)

cdef void* c_largest_squareish_histogram(int *histogram, int N, int row):
    return csquareish.largest_squareish_histogram(histogram, N, row)

cdef void* c_largest_squareish_matrix(double *histogram, int N, int M, double value):
    return csquareish.largest_squareish_matrix(histogram, N, M, value)

cdef int c_set_test(int test_val):
    return csquareish.largest_squareish_set_test(test_val)

def largest_squareish_histogram(numpy.ndarray[int, ndim=1, mode="c"] histogram not None, int row=0):
    cdef csquareish.Region* out = <csquareish.Region*>c_largest_squareish_histogram(<int*>histogram.data, histogram.shape[0], row)
    return dict(size=(<int>out.size_x, <int>out.size_y), location=(<int>out.loc_x, <int>out.loc_y))

def largest_squareish_matrix(numpy.ndarray[double, ndim=2, mode="c"] histogram not None, double value=0):
    cdef csquareish.Region* out = <csquareish.Region*>c_largest_squareish_matrix(<double*>histogram.data, <int>histogram.shape[0], <int>histogram.shape[1], value)
    return dict(size=(<int>out.size_x, <int>out.size_y), location=(<int>out.loc_x, <int>out.loc_y))

def solve_histogram(histo, row=0):
    return largest_squareish_histogram(numpy.asarray(histo, dtype=numpy.intc), row)

def solve_matrix(matrix_histo, value=0):
    return largest_squareish_matrix(numpy.asarray(matrix_histo, dtype=numpy.double), value)

def set_test(test_val=0):
    return c_set_test(test_val)