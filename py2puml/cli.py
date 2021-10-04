#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser

from py2puml.py2puml import py2puml


def run():
    argparser = ArgumentParser(description='Generate PlantUML class diagrams to document your Python application.')

    argparser.add_argument('-v', '--version', action='version', version='py2puml 0.5.2')
    argparser.add_argument('path', metavar='path', type=str, help='the path of the domain')
    argparser.add_argument('module', metavar='module', type=str, help='the module of the domain', default=None)

    args = argparser.parse_args()
    print(''.join(py2puml(args.path, args.module)))
