#include <stdio.h>
#include <stdlib.h>
#include "largest_squareish.h"

int test_histogram(int *in, int N, int size_x, int size_y, int loc_x) {
    int ret = 0;
    struct Region *maxRegion = largest_squareish_histogram(in, N, 0);
    if (maxRegion->size_x != size_x || maxRegion->size_y != size_y || maxRegion->loc_x != loc_x) {
        print_region(maxRegion);
        ret = -1;
    }
    free(maxRegion);
    return ret;
}

int test_matrix(double *in, int N, int M, int size_x, int size_y, int loc_x, int loc_y) {
    int ret = 0;
    struct Region *maxRegion = largest_squareish_matrix(in, N, M, 0);
    if (maxRegion->size_x != size_x || maxRegion->size_y != size_y || maxRegion->loc_x != loc_x || maxRegion->loc_y != loc_y) {
        print_region(maxRegion);
        ret = -1;
    }
    free(maxRegion);
    return ret;
}

int test_largest_squareish_histogram() {
    int ret;
    int test1[4] = {1,1,5,6};
    ret = test_histogram(test1, 4, 2, 5, 2);
    if (ret != 0) {
        printf("Failed test 1");
        return 1;
    }

    int test2[8] = {1,1,2,2,1,1,1,1};
    ret = test_histogram(test2, 8, 8, 1, 0);
    if (ret != 0) {
        printf("Failed test 2");
        return 2;
    }

    int test3[8] = {2,2,2,2,1,1,1,1};
    ret = test_histogram(test3, 8, 4, 2, 0);
    if (ret != 0) {
        printf("Failed test 3");
        return 3;
    }

    int test4[8] = {1,1,1,5,6,4,1,1};
    ret = test_histogram(test4, 8, 3, 4, 3);
    if (ret != 0) {
        printf("Failed test 4");
        return 4;
    }

    return 0;
}

int test_largest_squareish_matrix() {
    int ret;
    double test1[4] = {0,0,0,0};
    ret = test_matrix(test1, 2, 2, 2,2,0,0);
    if (ret != 0) {
        printf("Failed test 1");
        return 1;
    }
}

int main(void) {
    int ret;

    ret = test_largest_squareish_histogram();
    if (ret != 0) {
        printf("Failed histogram test %d\n", ret);
        return ret;
    }

    ret = test_largest_squareish_matrix();
    if (ret != 0) {
        printf("Failed matrix test %d\n", ret);
        return ret;
    }

    return 0;
}
