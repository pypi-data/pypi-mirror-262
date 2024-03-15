# -----------------------------------------------------------------------------
# TypeHub
# Copyright (c) 2023 Felipe Amaral dos Santos
# Licensed under the MIT License (see LICENSE file)
# -----------------------------------------------------------------------------

from setuptools import setup


desc = """TypeHub is a Python library for enhanced typing with 
custom annotations, extending standard types for more expressive and precise 
code."""

setup(
    author='Felipe Amaral',
    author_email='lipeamaralsantos@gmail.com',
    description=desc,
    install_requires=['colorama==0.4.4'],
    keywords='typing type typehub',
    name='TypeHub',
    packages=['typehub'],
    version='1.0.0a3'
)
