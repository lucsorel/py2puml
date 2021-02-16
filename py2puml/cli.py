#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from sys import argv

from py2puml.py2puml import py2puml
from py2puml import __version__, __description__

CLI_VERSION = f'py2puml {__version__}'
PATH_ARG_HELP = 'the path of the domain'
MODULE_ARG_HELP = 'the module of the domain'

# CLI end-point when py2puml is installed at the system level
def run():
    argparser = ArgumentParser(description=__description__)

    argparser.add_argument('-v', '--version', action='version', version=CLI_VERSION)
    argparser.add_argument('path', metavar='path', type=str, help=PATH_ARG_HELP)
    argparser.add_argument('module', metavar='module', type=str, help=MODULE_ARG_HELP, default=None)

    args = argparser.parse_args()
    print(''.join(py2puml(args.path, args.module)))

# CLI end-point when py2puml is NOT installed at the system level
if __name__ == '__main__':
    if len(argv) == 2 and argv[1] in ['-v', '--version']:
        print(f'{__description__} ({CLI_VERSION})')
    elif len(argv) == 3:
        print(''.join(py2puml(argv[1], argv[2])))
    else:
        raise ValueError(f'''
The CLI can be called in 2 ways:
- version: python -m py2puml.cli -v or python -m py2puml.cli --version
- plantuml documentation (2 mandatory arguments): `python py2puml.cli domain/path domain.module`: {PATH_ARG_HELP}, {MODULE_ARG_HELP}
''')
