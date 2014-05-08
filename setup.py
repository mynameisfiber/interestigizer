#!/usr/bin/env python
#
# Note: We use the setup.requires method of installing dependencies (as opposed
# to virtualenv's requirements.txt) because in order to have numpy/scipy
# reasonably install on heroku we use a custom buildpack [1].  This buildpack
# assumes that we specify dependencies this way and won't work otherwise [2]
#
# [1] https://github.com/heroku/heroku-buildpack-python
# [2] http://stackoverflow.com/questions/9819968/running-scipy-on-heroku

#from distutils.core import setup, Extension
#from setuptools import setup, Extension
import os
import numpy

try:
    from setuptools import setup, Extension
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, Extension

from Cython.Distutils import build_ext
from distutils.sysconfig import get_python_inc

try:
    os.makedirs("./tmp")
except:
    pass


setup(
    name='interestingizer',
    version='0.3.0',
    description='Turns ordinary images into interesting ones!',
    author='Micha Gorelick',
    author_email='mynameisfiber@gmail.com',
    url='http://github.com/fish2000/interestingizer/',

    ext_modules=[
        Extension('largest_squareish.squareish', [
            'largest_squareish/src/largest_squareish.c',
            'largest_squareish/squareish.pyx']),
    ],
    
    cmdclass=dict(build_ext=build_ext),
    include_dirs=[
        numpy.get_include(),
        get_python_inc(plat_specific=1),
        'largest_squareish/src'],
    
    install_requires = [
        "flask",
        "requests",
        "Pillow",
        "numpy",
        "scipy",
    ],
)
