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
    print "1) Premier League \n 2) Premiera Division \n 3) Ekstraklasa \n \n 0) Exit \n \n Select League or Exit:"
    while TRUE:
        select_league = raw_input()
        if selct_league in (0,1,2,3):
            break
        else:
            print "Unknown Command. Try again"

    if select_league == 1:
        league = 'PremierLeague'
        fpr = 10 # fixture per round
    if select_league == 2:
        league = 'PremieraDivision'
        fpr = 10
    if select_league == 3:
        league ='Ekstraklasa'
        fpr = 8
    if select_league == 0:
        break
 
    fixtures = getFixtures(league, fpr)
    dbInsertFixtures(league, fixtures)


def update():
    print "1) Premier League \n 2) Premiera Division \n 3) Ekstraklasa \n \n 0) Exit \n \n Select League or Exit:"
    while TRUE:
        select_league = raw_input()
        if selct_league in (0,1,2,3):
            break
        else:
            print "Unknown Command. Try again"

    if select_league == 1:
        league = 'PremierLeague'
    if select_league == 2:
        league = 'PremieraDivision'
    if select_league == 3:
        league ='Ekstraklasa'
    if select_league == 0:
        break
 
    results = getResults(league)
    dbUpdateResults(league, results)


if __name__ == '__main__':
    arguments = docopt(__doc__, version=__version__)
    if arguments['update']:
        update()
    elif arguments['insert']:
        insert()
