import numpy as np
from scipy import ndimage
import pylab as py

from PIL import Image, ImageOps
import largest_square as lq

import operator
import sys
import os
import time

N_SAMPLES = 600*400
DEBUG = False

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

def mul_list(a, b):
    return map(int, [operator.mul(*x) for x in zip(a,b)])

def rescale_image(img, samples=N_SAMPLES):
    with TimeBlock("Resampling"):
        box_area = img.size[1] * img.size[0] / samples
        box_length = np.sqrt(box_area)

        scale = 1,1
        if box_length > 0:
            new_size = map(int, map(lambda x : x / box_length, img.size))
            scale = [img.size[i]/float(new_size[i]) for i in range(len(new_size))]

            img = img.resize(new_size)
    return img, scale

def create_locator_inplace(data):
    with TimeBlock("Locating"):
        ndimage.gaussian_filter(data, 4, output=data)
        ndimage.gaussian_gradient_magnitude(data, 8, output=data)

def find_uninteresting(img, filename):
    img_scaled, scale = rescale_image(ImageOps.grayscale(img))
    data = np.array(img_scaled)

    create_locator_inplace(data)

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

def insert_interesting_inplace(image, interesting, interesting_loc, interesting_size):
    mid_inter = np.asarray([x / 2. for x in interesting.size])
    mid_best = np.asarray([x / 2. for x in interesting_size])
    offset = map(int, mid_best - mid_inter)
    if interesting_loc[0] + mid_best[0] > image.size[0] / 2:
        print "Flipping"
        interesting = interesting.transpose(Image.FLIP_LEFT_RIGHT)
    image.paste(interesting, (interesting_loc[0] + offset[0], interesting_loc[1] + offset[1]), interesting)

if __name__ == "__main__":
    image = sys.argv[1]
    interestingizer= sys.argv[2]

    img = Image.open(open(image))
    interesting = Image.open(open(interestingizer)).convert("RGBA")

    best_loc, best_size = find_uninteresting(img, image)

    with TimeBlock("Thumnailing interesting"):
        interesting.thumbnail(best_size)

    insert_interesting_inplace(img, interesting, best_loc, best_size)

    with TimeBlock("Saving"):
        name = os.path.basename(image)
        img.save("./final/%s.jpg" % name)

