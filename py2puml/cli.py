#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from py2puml.py2puml import py2puml
from py2puml import __version__


def run():
    argparser = argparse.ArgumentParser(description="Generate PlantUML diagrams to document your python code.")

    argparser.add_argument('-v', '--version', action='version',
                           version='py2puml {version}'.format(version=__version__))

    argparser.add_argument("path", metavar="path",
                           type=str,
                           help="the path of the domain.")

    argparser.add_argument("module", metavar="module",
                           type=str,
                           help="the module of the domain.",
                           default=None)

    args = argparser.parse_args()

    print(''.join(
        py2puml(args.path, args.module)
    ))
