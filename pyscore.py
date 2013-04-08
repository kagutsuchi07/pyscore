#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""pyscore

Usage:
    pyscore insert
    pyscore update
    pyscore -h | --help | --version

Options:
    -h --help  Show this screen.
    --version  Show version.

"""

__title__ = 'pyscore'
__version__ = '0.0.1'

from docopt import docopt

from fixtures import insert_values, update_values


def insert():
    insert_values()


def update():
    update_values()


if __name__ == '__main__':
    arguments = docopt(__doc__, version=__version__)
    if arguments['update']:
        update()
    elif arguments['insert']:
        insert()
