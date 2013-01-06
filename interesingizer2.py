import numpy as np
from scipy import ndimage
import pylab as py

from PIL import Image, ImageOps
import largest_square as lq

import operator
import sys
import os

def drawrectangle(image, X, size):
    c = 0
    for x in range(X[0], X[0]+size[0]):
        for y in range(X[1], X[1]+size[1]):
            try:
                image[x,y] /= 10.
                c += 1
            except Exception, e:
                print e
                pass
    print "Drew %d blocks" % c

N_SAMPLES = 600*400

def mul_list(a, b):
    return map(int, [operator.mul(*x) for x in zip(a,b)])

def find_uninteresting(img, filename):
    data = np.array(img)
    print "Resampling"
    box_area = data.shape[0] * data.shape[1] / N_SAMPLES
    box_length = np.sqrt(box_area)
    scale = 1,1
    if box_length > 0:
        width, height = map(int, map(lambda x : x / box_length, data.shape[:-1]))
        scale = data.shape[0] / float(width), data.shape[1] / float(height)

        img_small = ImageOps.grayscale(img.resize((height, width)))
        data = np.array(img_small)
    else:
        img = ImageOps.grayscale(img)
        data = np.array(img)

    print "locationifying"
    blur = ndimage.gaussian_filter(data, 4)
    locator = ndimage.gaussian_gradient_magnitude(blur, 8)

    print "Finding squares"
    sq_size, sq_loc = lq.max_size(locator, locator.min())
    print sq_size, sq_loc

    print "Plotting"
    py.figure()
    py.title("Original")
    drawrectangle(data, sq_loc, sq_size)
    py.imshow(data, interpolation=None)
    py.colorbar()
    py.savefig("%s-interesting.png" % filename)

    py.figure()
    py.title("locator")
    py.imshow(locator, interpolation=None)
    py.colorbar()
    py.savefig("%s-interesting-locator.png" % filename)

    return mul_list(sq_size, scale), mul_list(sq_loc, scale)

if __name__ == "__main__":
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]

    img = Image.open(open(filename1))
    interesting = Image.open(open(filename2)).convert("RGBA")

    best_size, best_loc = find_uninteresting(img, filename1)
    print best_size, best_loc
    interesting.thumbnail([best_size[1], best_size[0]])

    print "interestingilizing"
    mid_inter = np.asarray([x / 2. for x in reversed(interesting.size)])
    mid_best = np.asarray([x / 2. for x in best_size])
    offset = map(int, mid_best - mid_inter)

    print best_loc, img.size
    if best_loc[1] + mid_best[1] > img.size[0] / 2:
        print "Flipping"
        interesting = interesting.transpose(Image.FLIP_LEFT_RIGHT)

    img.paste(interesting, (best_loc[1] + offset[1], best_loc[0] + offset[0]), interesting)

    print "saving"
    name = os.path.basename(filename1)
    img.save("./final/%s.jpg" % name)

