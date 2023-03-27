#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from pathlib import Path
from sys import path

from py2puml.py2puml import py2puml


def run():
    # adds the current working directory to the system path so that py2puml can import them
    current_working_directory = str(Path.cwd().resolve())
    if current_working_directory not in path:
        path.append(current_working_directory)

    argparser = ArgumentParser(description='Generate PlantUML class diagrams to document your Python application.')

    argparser.add_argument('-v', '--version', action='version', version='py2puml 0.7.2')
    argparser.add_argument('path', metavar='path', type=str, help='the filepath to the domain')
    argparser.add_argument('module', metavar='module', type=str, help='the module name of the domain', default=None)

    args = argparser.parse_args()
    print(''.join(py2puml(args.path, args.module)))
