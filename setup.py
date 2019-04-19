#!/usr/bin/env python

"""
Setup script for shipdataprocess
"""

import codecs
import os

from setuptools import find_packages
from setuptools import setup

package = __import__('shipdataprocess')

DEPENDENCIES = [
    "pytest",
    "unidecode",
    "roman",
    "Django"
]

with codecs.open('README.md', encoding='utf-8') as f:
    readme = f.read().strip()

setup(
    author=package.__author__,
    author_email=package.__email__,
    description=package.__doc__.strip(),
    include_package_data=True,
    install_requires=DEPENDENCIES,
    keywords=['ship','vessel','fishing','normalization'],
    license="Apache 2.0",
    long_description=readme,
    name='shipdataprocess',
    packages=find_packages(exclude=['test*.*', 'tests']),
    url=package.__source__,
    version=package.__version__,
    zip_safe=True,
)

