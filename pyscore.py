#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""pyscore

Usage:
    pyscore update
    pyscore -h | --help | --version

Options:
    -h --help  Show this screen.
    --version  Show version.

"""

__title__ = 'pyscore'
__version__ = '0.0.1'

from docopt import docopt


def update():
    return 'TEST'


if __name__ == '__main__':
    arguments = docopt(__doc__, version=__version__)
    if arguments['update']:
        print update()
