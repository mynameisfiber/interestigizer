#!/usr/bin/env python2.7

import numpy as np
from scipy import ndimage
from PIL import Image
from collections import Counter

def drawrectangle(image, x0, x1):
    print x0, x1
    for x in range(x0[0], x1[0]):
        for y in range(x0[1], x1[1]):
            try:
                image[x,y,:] /= 2
            except:
                pass

def regionarea(region):
    return (region[0].start-region[1].start)*(region[0].stop-region[1].stop)

if __name__ == "__main__":
    img = Image.open(open("./test/502006d1296665315-timelesshd-papohaku-beach.png"))

    # We do the mean in order to get a monochromatic image
    data = np.array(img)

    locator = ndimage.gaussian_laplace(data.mean(axis=2), sigma=0.5)
    #locator = ndimage.gaussian_filter(data, sigma=1)

    #blur = ndimage.sobel(ndimageear
    #locator = ndimage.gaussian_filter(ndimage.laplace(blur), sigm

    #locator *= np.log(locator)
    threshold = locator.mean() - 0.5 * locator.std()

    locator[ locator > threshold ] = 0

    labels, nlabels = ndimage.label(locator)
    regions = ndimage.find_objects(labels)
    com = ndimage.center_of_mass(locator, labels, range(nlabels))

    region_values = {}
    for i, region in enumerate(regions):
        region_values[i] = {
            "mean" : locator[region].mean(),
            "com" : com[i],
            "area" : regionarea(regions[i]),
            "box" : regions[i],
        }

    #ordered_regions = sorted(range(nlabels), key=lambda x : region_values[x]["mean"] / region_values[x]["area"], reverse=False)
    ordered_regions = []
    for idx, count in Counter(labels.flatten()).most_common():
        try:
            ordered_regions.append(region_values[idx])
            region_values[idx]["num_pixels"] = count
        except:
            pass

    for region in ordered_regions[:5]:
        c = region["box"]
        drawrectangle(data, (c[0].start, c[0].stop), (c[1].start, c[1].stop))

    Image.fromarray(np.uint8(data)).save(open("test.png", "w+"))





