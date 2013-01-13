#!/usr/bin/env python

from distutils.core import setup, Extension

setup(
    name = 'interestingizer',
    version = '0.1',
    description = 'Turns ordinary images into interesting ones!',
    author = 'Micha Gorelick',
    author_email = 'mynameisfiber@gmail.com',
    url = 'http://github.com/mynameisfiber/interestingizer/',

    ext_modules = [
        Extension('largest_squareish.interestingizer', ['largest_squareish/src/largest_squareish.c']),
    ],
)
