#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fixtures import getFixtures, getResults, dbInsertFixtures, dbUpdateResults


def menu():
    print '''pyscore version 0.0.2

1) Insert
2) Update

0) Exit'''

    select_menu = 0

    while True:
        select_menu = raw_input("Select option or Exit: ")
        if select_menu in ('0', '1', '2'):
            break
        else:
            print "Unknown Command. Try again"

    if select_menu == '1':
        menu = 1
        print 'INSERT'
    elif select_menu == '2':
        menu = 2
        print 'UPDATE'
    elif select_menu == '0':
        return 0

    print '''
1) Premier League
2) Premiera Division
3) Ekstraklasa

0) Exit to Menu'''

    select_league = 0

    while True:
        select_league = raw_input("Select League or Exit: ")
        if select_league in ('0', '1', '2', '3'):
            break
        else:
            print "Unknown Command. Try again"

    if select_league == '1':
        league = ['Premier League', '2012/2013']
    elif select_league == '2':
        league = ['Premiera Division', '2012/2013']
    elif select_league == '3':
        league = ['Ekstraklasa', '2012/2013']
    elif select_league == '0':
        menu()

    if menu == 1:
        insert(league)
    elif menu == 2:
        update(league)


def insert(league):
    fixtures = getFixtures(league)
    dbInsertFixtures(league, fixtures)


def update(league):
    results = getResults(league)
    dbUpdateResults(results, league)


if __name__ == '__main__':
    menu()
