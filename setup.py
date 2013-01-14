#!/usr/bin/env python
#
# Note: We use the setup.requires method of installing dependencies (as opposed
# to virtualenv's requirements.txt) because in order to have numpy/scipy
# reasonably install on heroku we use a custom buildpack [1].  This buildpack
# assumes that we specify dependencies this way and won't work otherwise [2]
#
# [1] https://github.com/heroku/heroku-buildpack-python
# [2] http://stackoverflow.com/questions/9819968/running-scipy-on-heroku

from distutils.core import setup, Extension
import os

try:
    os.makedirs("./tmp")
except:
    pass

setup(
    name = 'interestingizer',
    version = '0.1',
    description = 'Turns ordinary images into interesting ones!',
    author = 'Micha Gorelick',
    author_email = 'mynameisfiber@gmail.com',
    url = 'http://github.com/mynameisfiber/interestingizer/',

    ext_modules = [
        Extension('largest_squareish.largest_squareish', 
            ['largest_squareish/src/largest_squareish.c']),
    ],

    requires = [
        "PIL",
        "numpy",
        "scipy",
        "flask",
    ],
)

