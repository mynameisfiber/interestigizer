import numpy as np
from scipy import ndimage

from PIL import Image, ImageOps
import largest_squareish as lq

import operator
import sys
import os

N_SAMPLES = 1024*768 #600*400

def mul_list(a, b):
    return map(int, [operator.mul(*x) for x in zip(a,b)])

def rescale_image(img, samples=N_SAMPLES):
    box_area = img.size[1] * img.size[0] / samples
    box_length = np.sqrt(box_area)

    scale = 1,1
    if box_length > 0:
        new_size = map(int, map(lambda x : x / box_length, img.size))
        scale = [img.size[i]/float(new_size[i]) for i in range(len(new_size))]

        img = img.resize(new_size)
    return img, scale

def create_locator_inplace(data):
    ndimage.gaussian_filter(data, 4, output=data)
    ndimage.gaussian_gradient_magnitude(data, 8, output=data)

def find_uninteresting(img):
    img_scaled, scale = rescale_image(ImageOps.grayscale(img))
    data = np.array(img_scaled)

    create_locator_inplace(data)

    boring_area = lq.solve_matrix(data, data.min())

    # Convert coordinates to PIL syntax (y, x) and scale
    pil_size = mul_list(reversed(boring_area["size"]), scale)
    pil_loc = mul_list(reversed(boring_area["location"]), scale)
    return pil_loc, pil_size

def insert_interesting_inplace(image, interesting, interesting_loc, interesting_size):
    mid_inter = np.asarray([x / 2. for x in interesting.size])
    mid_best = np.asarray([x / 2. for x in interesting_size])
    offset = map(int, mid_best - mid_inter)
    if interesting_loc[0] + mid_best[0] > image.size[0] / 2:
        interesting = interesting.transpose(Image.FLIP_LEFT_RIGHT)
    image.paste(interesting, (interesting_loc[0] + offset[0], interesting_loc[1] + offset[1]), interesting)

def interestingize(image, interesting):
    best_loc, best_size = find_uninteresting(image)
    interesting.thumbnail(best_size)
    insert_interesting_inplace(image, interesting, best_loc, best_size)
    return image

if __name__ == "__main__":
    image = sys.argv[1]
    interestingizer= sys.argv[2]

    img = Image.open(open(image))
    interesting = Image.open(open(interestingizer)).convert("RGBA")

    img = interestingize(img, interesting)
    name = os.path.basename(image)
    img.save("./final/%s.jpg" % name)

