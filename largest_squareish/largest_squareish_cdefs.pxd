
cdef extern from "./src/largest_squareish.h":
    cdef struct Region:
        int size_x
        int size_y
        int loc_x
        int loc_y
    
    cdef struct Stack:
        pass
    
    #int largest_squareish_set_test(int set)
    void print_region(Region* reg)
    void* largest_squareish_histogram(int* histogram, int N, int row)
    void* largest_squareish_matrix(double* histogram, int N, int M, double value)
    
    double area(int x, int y)
    bint is_larger(Region* maxRegion, Region* other)
    bint is_larger_params(Region* maxRegion, int start, int pos, int height)