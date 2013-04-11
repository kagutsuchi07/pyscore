#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""pyscore

Usage:
    pyscore insert
    pyscore update
    pyscore --leagues
    pyscore -h | --help | --version

Options:
    -h --help  Show this screen.
    --version  Show version.
    --leagues  List all avaible leagues.

"""

__title__ = 'pyscore'
__version__ = '0.0.1'

from docopt import docopt

from config import leagues
from fixtures import getFixtures, getResults, dbInsertFixtures, dbUpdateResults


def show_leagues():
    for id in leagues:
        print '%s. %s' % (id, leagues[id])


def menu_choose_league():
    show_leagues()
    while True:
        try:
            id = int(raw_input())
        except ValueError:
            print 'Invalid ID. Try again.'
            continue

        if id not in leagues.keys():
            print 'Unknown ID. Try again.'
        return leagues[id]


def insert(league_name):
    fixtures = getFixtures(league_name)
    dbInsertFixtures(league_name, fixtures)


def update(league_name):
    results = getResults(league_name)
    dbUpdateResults(league_name, results)


if __name__ == '__main__':
    arguments = docopt(__doc__, version=__version__)
    if arguments['--leagues']:
        show_leagues()
    elif arguments['update']:
        update(menu_choose_league())
    elif arguments['insert']:
        insert(menu_choose_league())
