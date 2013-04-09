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

from fixtures import getFixtures, getResults, dbInsertFixtures, dbUpdateResults


def insert():
    fixtures = getFixtures()
    dbInsertFixtures(fixtures)


def update():
    results = getResults()
    dbUpdateResults(results)


if __name__ == '__main__':
    arguments = docopt(__doc__, version=__version__)
    if arguments['update']:
        update()
    elif arguments['insert']:
        insert()
