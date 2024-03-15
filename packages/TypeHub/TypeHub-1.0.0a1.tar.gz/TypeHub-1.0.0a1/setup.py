# -----------------------------------------------------------------------------
# TypeHub
# Copyright (c) 2023 Felipe Amaral dos Santos
# Licensed under the MIT License (see LICENSE file)
# -----------------------------------------------------------------------------

from setuptools import setup
from version import __author__, __description__, __version__  


setup(
    author=__author__,
    author_email='lipeamaralsantos@gmail.com',
    description=__description__,
    install_requires=['colorama==0.4.4'],
    keywords='typing type typehub',
    name='TypeHub',
    packages=['typehub'],
    version=__version__
)