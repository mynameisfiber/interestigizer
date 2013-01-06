#!/usr/bin/env python2.7

import numpy as np
from scipy import ndimage
from PIL import Image
import pylab as py
import mahotas
import operator
import largest_square as lq
import sys

def drawrectangle(image, X, size):
    for x in range(X[0], X[0]+size[0]):
        for y in range(X[1], X[1]+size[1]):
            try:
                image[x,y,:] = 25
            except:
                pass

def regionarea(region):
    return (region[0].start-region[0].stop)*(region[1].start-region[1].stop)

if __name__ == "__main__":
    filename = sys.argv[1]
    print "Reading"
    img = Image.open(open(filename))

    box_area = data.shape[0] * data.shape[1] / N_SAMPLES
    box_length = np.sqrt(box_area)
    width, height, _ = map(int, map(lambda x : x / box_length, data.shape))
    img = img.resize((height, width))

    # We do the mean in order to get a monochromatic image
    data = np.array(img)
    data_2d = data.sum(axis=-1)

    print "Sobel"
    sx = ndimage.sobel(data_2d, axis=0, mode='constant')
    sy = ndimage.sobel(data_2d, axis=1, mode='constant')
    sob = np.hypot(sx, sy)
    sob_gradmag = ndimage.gaussian_gradient_magnitude(sob, sigma=1.0)

    locator = sob_gradmag.astype(np.uint64)

    print "Locating"
    T = mahotas.thresholding.otsu(locator)
    labels, n_labels = mahotas.label(locator < T, Bc=np.ones((50,50)))

    labels_max = mahotas.labeled.labeled_max(locator, labels)
    labels_sum = mahotas.labeled.labeled_sum(locator, labels)
    labels_area = mahotas.labeled.labeled_size(labels)

    # using sobel density as a metric
    #labels_metric = labels_sum * np.log(labels_area) / labels_area
    #metric_loc, metric_val = min(enumerate(labels_metric), key=operator.itemgetter(1))

    labels_metric = labels_max * labels_area
    metric_loc, metric_val = max(enumerate(labels_metric), key=operator.itemgetter(1))

    print "Finding squares"
    sq_size, sq_loc = lq.max_size(labels, metric_loc)
    print sq_size, sq_loc

    print "Plotting"
    py.figure()
    py.title("Original")
    py.imshow(data, interpolation=None)
    drawrectangle(data, sq_loc, sq_size)
    py.colorbar()
    py.savefig("%s-interesting.png" % filename)

    #py.figure()
    #py.title("Locator")
    #py.imshow(locator, interpolation=None)
    #py.colorbar()

    #py.figure()
    #py.title("labels")
    #drawrectangle(labels, sq_loc, sq_size)
    #py.imshow(labels, interpolation=None)
    #py.colorbar()

    #for i in range(n_labels+1):
        #py.figure()
        #py.title("label = %d"%i)
        #d = data_2d.copy()
        #d[labels == i] = 0
        #py.imshow(d, interpolation=None)
        #py.colorbar()





