#!env python
import re
from setuptools import setup
from glob import glob

setup(
    name            = 'videopoker',
    version         = '1.0',
    description     = 'video poker game',
    author          = 'kortox',
    author_email    = 'kortox@gmail.com',
    url             = 'https://github.com/kortox/videopoker',
    packages        = ['videopoker'],
    scripts         = glob('bin/*'),
)
