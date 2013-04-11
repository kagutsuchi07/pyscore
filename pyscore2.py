#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fixtures import getFixtures, getResults, dbInsertFixtures, dbUpdateResults

def menu():

    print """pyscore version 0.0.1

1) Insert
2) Update

0) Exit
    """

    selct_menu = 0

    while True:
        select_menu = raw_input("Select option or Exit: ")
        if selct_menu in (0,1,2):
            break
        else:
            print "Unknown Command. Try again"

    if select_menu == '1':
        insert()
    elif select_menu == '2':
        update()
    elif select_menu == '0':
        return 0

def insert():
    print  """
INSERT

1) Premier League
2) Premiera Division
3) Ekstraklasa

0) Exit to Menu
    """

    select_league = 0
    
    while True:
        select_league = raw_input("Select League or Exit: ")
        if select_league in ('0','1','2','3'):
            break
        else:
            print "Unknown Command. Try again"

    if select_league == '1':
        league = 'PremierLeague'
        fpr = 10 # fixture per round
    elif select_league == '2':
        league = 'PremieraDivision'
        fpr = 10
    elif select_league == '3':
        league ='Ekstraklasa'
        fpr = 8
    elif select_league == '0':
        menu()
 
    fixtures = getFixtures(league, fpr)
    dbInsertFixtures(league, fixtures)


def update():
    print  """UPDATE

1) Premier League
2) Premiera Division
3) Ekstraklasa

0) Exit to Menu
    """

    select_league = 0

    while True:
        select_league = raw_input("Select League or Exit: ")
        if select_league in ('0','1','2','3'):
            break
        else:
            print "Unknown Command. Try again"

    if select_league == '1':
        league = 'PremierLeague'
    elif select_league == '2':
        league = 'PremieraDivision'
    elif select_league == '3':
        league ='Ekstraklasa'
    elif select_league == '0':
        menu()
 
    results = getResults(league)
    dbUpdateResults(results, league)


menu()
