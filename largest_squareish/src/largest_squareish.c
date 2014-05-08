#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "largest_squareish.h"

int LQISH_TEST = 0;
int largest_squareish_set_test(int test_val) {
    LQISH_TEST = test_val;
    return LQISH_TEST;
}

void print_region(struct Region *reg) {
    printf("{%d, %d, %d, %d}\n", reg->size_x, reg->size_y, reg->loc_x, reg->loc_y);
}

void *largest_squareish_histogram(int *histogram, int N, int row) {
    struct Stack *topStack = NULL;
    struct Stack *lastStack = topStack;

    struct Region *maxRegion = malloc(sizeof(struct Region));
    maxRegion->size_x = 0;
    maxRegion->size_y = 0;
    maxRegion->loc_x = 0;

    int height;
    int pos, start;
    for(pos = 0; pos <= N; pos++) {
        height = pos == N ? 0 : histogram[pos]; // we need one extra iteration for boundary cases
        start = pos;
        while (1) {
            if (lastStack == NULL || height > lastStack->data->size_y) {
                struct Region *element = malloc(sizeof(struct Region));
                element->size_x = pos - start;
                element->size_y = height;
                element->loc_x = start;

                struct Stack *newStackElem = malloc(sizeof(struct Stack));
                newStackElem->data = element;
                newStackElem->next = NULL;
                newStackElem->prev = NULL;
                if (lastStack != NULL) {
                    newStackElem->prev = lastStack;
                    lastStack->next = newStackElem;
                } else {
                    topStack = newStackElem;
                }
                lastStack = newStackElem;
            } else if (lastStack->data != NULL && height < lastStack->data->size_y) {
                start = lastStack->data->loc_x;
                int cur_y = lastStack->data->size_y;
                if (is_larger_params(maxRegion, start, pos, cur_y) > 0) {
                    maxRegion->size_x = pos - start;
                    maxRegion->size_y = cur_y;
                    maxRegion->loc_x = start;
                }

                if (lastStack->prev == NULL) {
                    free(lastStack->data);
                    free(lastStack);
                    lastStack = NULL;
                    topStack = NULL;
                } else {
                    struct Stack *tmp = lastStack->prev;
                    tmp->next = NULL;
                    free(lastStack->data);
                    free(lastStack);
                    lastStack = tmp;
                }
                continue;
            }
            break;
        }
    }
    pos += 1;
    struct Stack *curStack = topStack;
    while (curStack != NULL) {
        if (curStack->data != NULL) {
            if (is_larger(maxRegion, curStack->data) > 0) {
                maxRegion->size_x = curStack->data->size_x;
                maxRegion->size_y = curStack->data->size_y;
                maxRegion->loc_x = curStack->data->loc_x;
            }
            free(curStack->data);
        }
        topStack = curStack;
        curStack = topStack->next;
        free(topStack);
    }
    maxRegion->loc_y = maxRegion->size_y;
    return maxRegion;
}

void *largest_squareish_matrix(double *histogram, int N, int M, double value) {
    struct Region *maxRegion = malloc(sizeof(struct Region));
    maxRegion->size_x = 0;
    maxRegion->size_y = 0;
    maxRegion->loc_x = 0;
    maxRegion->loc_y = 0;
    int *scanline = malloc(sizeof(int)*M);

    int m;
    for (m=0; m<M; m++) {
        scanline[m] = 0;
    }

    int n;
    for (n=0; n<N; n++) {
        for (m=0; m<M; m++) {
            if (histogram[n*M + m] == value)
                scanline[m] += 1;
            else
                scanline[m] = 0;
        }
        struct Region *newRegion = largest_squareish_histogram(scanline, M, n);
        newRegion->loc_y = n + 1 - newRegion->loc_y;
        if (maxRegion == NULL || is_larger(maxRegion, newRegion) > 0) {
            maxRegion->size_x = newRegion->size_x;
            maxRegion->size_y = newRegion->size_y;
            maxRegion->loc_x = newRegion->loc_x;
            maxRegion->loc_y = newRegion->loc_y;
        }
        free(newRegion);
    }
    free(scanline);
    return maxRegion;
}

double inline area(int x, int y) {
    if (LQISH_TEST == 1) {
        return x*y; 
    } else {
        return x*y / pow(fabs(x - y) + 1, 1.5);
    }
}

int is_larger(struct Region *maxRegion, struct Region *other) {
    double max_area = area(maxRegion->size_x, maxRegion->size_y);
    double other_area = area(other->size_x, other->size_y);
    return (other_area - max_area) > 0;
}

int is_larger_params(struct Region *maxRegion, int start, int pos, int height) {
   double max_area = area(maxRegion->size_x, maxRegion->size_y);
   double other_area = area(pos-start, height);
   return (other_area - max_area) > 0;
}
