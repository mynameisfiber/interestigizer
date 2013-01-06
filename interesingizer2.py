import numpy as np
from scipy import ndimage
import pylab as py

from PIL import Image, ImageOps
import largest_square as lq

import operator
import sys
import os
import time

class TimeBlock:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.start = time.time()
        print "Entering block: %s" % self.name

    def __exit__(self, t, value, traceback):
        print "Block %s took: %fs" % (self.name, time.time() - self.start)
        return True

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
DEBUG = False

def mul_list(a, b):
    return map(int, [operator.mul(*x) for x in zip(a,b)])

def find_uninteresting(img, filename):
    with TimeBlock("Resampling"):
        box_area = img.size[1] * img.size[0] / N_SAMPLES
        box_length = np.sqrt(box_area)
        scale = 1,1

        if box_length > 0:
            new_size = map(int, map(lambda x : x / box_length, img.size))
            scale = [img.size[i]/float(new_size[i]) for i in range(len(new_size))]

            img_small = ImageOps.grayscale(img.resize(new_size))
            data = np.array(img_small)
        else:
            img = ImageOps.grayscale(img)
            data = np.array(img)

    with TimeBlock("Locating"):
        ndimage.gaussian_filter(data, 4, output=data)
        ndimage.gaussian_gradient_magnitude(data, 8, output=data)

    with TimeBlock("Squarifying"):
        sq_loc, sq_size = lq.max_size(data, data.min())

    if DEBUG:
        with TimeBlock("Plotting"):
            py.figure()
            py.title("locator")
            drawrectangle(data, sq_loc, sq_size)
            py.imshow(data, interpolation=None)
            py.colorbar()
            py.savefig("%s-interesting-locator.png" % filename)

    # Convert coordinates to PIL syntax (y, x) and scale
    pil_size = mul_list(reversed(sq_size), scale)
    pil_loc = mul_list(reversed(sq_loc), scale)
    return pil_loc, pil_size

if __name__ == "__main__":
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]

    img = Image.open(open(filename1))
    interesting = Image.open(open(filename2)).convert("RGBA")

    with TimeBlock("Finding lame region"):
        best_loc, best_size = find_uninteresting(img, filename1)

    with TimeBlock("Thumnailing interesting"):
        interesting.thumbnail(best_size)

    mid_inter = np.asarray([x / 2. for x in interesting.size])
    mid_best = np.asarray([x / 2. for x in best_size])
    offset = map(int, mid_best - mid_inter)

    if best_loc[0] + mid_best[0] > img.size[0] / 2:
        print "Flipping"
        interesting = interesting.transpose(Image.FLIP_LEFT_RIGHT)

    img.paste(interesting, (best_loc[0] + offset[0], best_loc[1] + offset[1]), interesting)

    with TimeBlock("Saving"):
        name = os.path.basename(filename1)
        img.save("./final/%s.jpg" % name)

