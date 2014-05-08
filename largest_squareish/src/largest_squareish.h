#ifndef _LARGEST_SQAUREISH_H
struct Region {
    int size_x;
    int size_y;

    int loc_x;
    int loc_y;
};

struct Stack {
    struct Region *data;
    struct Stack *next;
    struct Stack *prev;
};

int largest_squareish_set_test(int test_val);
void print_region(struct Region *reg);

void *largest_squareish_histogram(int *histogram, int N, int row);
void *largest_squareish_matrix(double *histogram, int N, int M, double value);

double inline area(int x, int y);
int is_larger(struct Region *maxRegion, struct Region *other);
int is_larger_params(struct Region *maxRegion, int start, int pos, int height);


#define _LARGEST_SQUAREISH_H
#endif
