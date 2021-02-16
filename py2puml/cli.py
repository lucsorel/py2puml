#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser

from py2puml.py2puml import py2puml
from py2puml import __version__, __description__

CLI_VERSION = f'py2puml {__version__}'
PATH_ARG_HELP = 'the path of the domain'
MODULE_ARG_HELP = 'the module of the domain'


def run():
    argparser = ArgumentParser(description=__description__)

    argparser.add_argument('-v', '--version', action='version', version=CLI_VERSION)
    argparser.add_argument('path', metavar='path', type=str, help=PATH_ARG_HELP)
    argparser.add_argument('module', metavar='module', type=str, help=MODULE_ARG_HELP, default=None)

    args = argparser.parse_args()
    print(''.join(py2puml(args.path, args.module)))
