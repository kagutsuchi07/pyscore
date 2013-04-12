import requests
import re
import torndb

from dateutil import parser
from config import db_host, db_database, db_user, db_pass

# DATABASE VALUES (Fixture, Round, First_Team, FT_Score, Second_Team, ST_Score, Match_Date(y-m-d 16:00:00)


# === DB
def dbInsertFixtures(league, fixtures):
    """Inserts all fixtures into database.

    :param league: List with league name and season.
    :param fixtures: List of fixtures.
    """
    db = torndb.Connection(db_host, db_database, db_user, db_pass)

    for fixture in fixtures:
        db.execute('''INSERT INTO Leagues (League, Season, Round, Home_Team, Away_Team, Match_Date)
            VALUES(%s, %s, %s, %s, %s, %s)''', league[0], league[1], fixture['nr_round'], fixture['ht'], fixture['at'], fixture['md'])
        print fixture['nr_round'], fixture['ht'], fixture['at'], fixture['md']

    db.close()


def dbUpdateResults(league, results):
    """Updates all results in database.

    :param results: List of results.
    """
    db = torndb.Connection(db_host, db_database, db_user, db_pass)

    for result in results:
        db_values = db.get('''SELECT Home_Score, Away_Score FROM Leagues
            WHERE League = %s AND Season = %s"''', league[0], league[1])
        db_fts = db_values['Home_Score']
        db_sts = db_values['Away_Score']
 
        if db_fts == result['hs'] and db_sts == result['as']:
            print result['ft'], resutlt['st'], 'OK'
        else:
            db.execute('''UPDATE Leagues SET Home_Score = %s, Away_Score = %s Match_Date = %s
                WHERE League = %s AND Season = %s AND Home_Team = %s AND Away_Team = %s
                ''', result['hs'], result['as'], result['md'], league[0], league[1], result['ht'], result['at'])
            print result[ht], result[at], '...UPDATED'

    db.close()
# === DB end


def getFixtures(league):
    """Returns all fixtures."""
    fixtures = []

    if league[0] == 'Premier League':
        pattern_league = 'http://www.bukmacherzy.com/liga_angielska/terminarz/'
    if league[0] == 'Premiera Division':
        pattern_league = 'http://www.bukmacherzy.com/liga_hiszpanska/terminarz/'
    if league[0] == 'Ekstraklasa':
        pattern_league = 'http://www.bukmacherzy.com/ekstraklasa/terminarz/'

    rc = requests.get(pattern_league).content
    rounds = int(re.findall('<strong>Kolejka: ([0-9]{2})</strong>', rc)[-1])
    rc = re.findall('<div class="data">(.+)</div><div class="godzina">(.+)</div> .+ title="Typy (.+)\-(.+)">', rc)
    fpr = len(rc)/rounds

    start = 0
    end = fpr
    match_id = 1
    for round in range(1, rounds+1):
        for data in rc[start:end]:
            fixtures.append({
                'nr_round': round,
                'ht': data[2],
                'at': data[3],
                'md': parser.parse(data[0] + ' ' + data[1])  # TODO: timezone
            })
            match_id += 1
        start += fpr
        end += fpr
    return fixtures


def getResults(league):
    """Returns all results."""
    results = []
 
    if league[0] == 'Premier League':
        pattern_league = 'http://www.bukmacherzy.com/liga_angielska/terminarz/'
    if league[0] == 'Premiera Division':
        pattern_league = 'http://www.bukmacherzy.com/liga_hiszpanska/terminarz/'
    if league == 'Ekstraklasa':
        pattern_league = 'http://www.bukmacherzy.com/ekstraklasa/terminarz/'

    rc = requests.get(pattern_league).content
    pattern_update = re.findall('<div class="data">(.+)</div><div class="godzina">(.+)</div> .+ title="Typy (.+)\-(.+)"> .+ <strong>(.+?)</strong>', rc)
 
    nr_match = 1

    for value in pattern_update:

        match_date = parse(value[0] + ' ' + value[1])

        result = {
            'ht': value[2],
            'hs': int(value[4][0]),
            'at': value[3],
            'as': int(value[4][2]),
            'md': match_date,
        }
        results.append(result)
 
        nr_match += 1
 
    return results
