#!/usr/bin/env python

from setuptools import setup

from py2puml import __version__

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(name='py2puml',
    version=__version__,
    description='Generate Plantuml diagrams to document your python code',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Luc Sorel-Giffo',
    url='https://github.com/lucsorel/py2puml',
    packages=list(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
