import requests
import re
import torndb
from dateutil import parser

from config import db_host, db_database, db_user, db_pass

# DATABASE VALUES (Fixture, Round, First_Team, FT_Score, Second_Team, ST_Score, Date(y-m-d 16:00:00)


# === DB
def dbInsertFixtures(league, fixtures):
    """Inserts all fixtures into database.

    :param fixtures: List of fixtures.
    """
    db = torndb.Connection(db_host, db_database, db_user, db_pass)

    for fixture in fixtures:
        db.execute("INSERT INTO %s VALUES(%s, %s, %s, NULL, %s, NULL, %s)", league, fixture['nr_match'], fixture['nr_round'], fixture['ft'], fixture['st'], fixture['md'])
        print fixture['nr_match'], fixture['nr_round'], fixture['ft'], 'NULL', fixture['st'], fixture['md']

    db.close()


def dbUpdateResults(league, results):
    """Updates all results in database.

    :param results: List of results.
    """
    db = torndb.Connection(db_host, db_database, db_user, db_pass)

    for result in results:
        db_values = db.get("SELECT FT_Score, ST_Score FROM %s WHERE Fixture=%s", league, result['nr_match'])
        db_fts = db_values['FT_Score']
        db_sts = db_values['ST_Score']

        if db_fts == result['fts'] and db_sts == result['sts']:
            print 'OK'
        else:
            db.execute("UPDATE %s SET FT_Score = %s, ST_Score = %s Match_Date = %s WHERE First_Team = %s AND Second_Team = %s", league, result['fts'], result['sts'], result['ft'], result['md'], result['st'])

        print 'Fixture: ', result['nr_match'], "First Team Score: ", result['fts'], 'Second Team Score: ', result['sts'], '...UPDATED'

    db.close()
# === DB end


def getFixtures(league):
    """Returns all fixtures."""
    fixtures = []

    if league == 'PremierLeague':
        pattern_league = 'http://www.bukmacherzy.com/liga_angielska/terminarz/'
    if league == 'PremieraDivision':
        pattern_league = 'http://www.bukmacherzy.com/liga_hiszpanska/terminarz/'
    if league == 'Ekstraklasa':
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
                'nr_match': match_id,
                'nr_round': round,
                'ft': data[2],
                'st': data[3],
                'md': parser.parse(data[0] + ' ' + data[1])  # TODO: timezone
            })
            match_id += 1
        start += fpr
        end += fpr
    return fixtures


def getResults(league):
    """Returns all results."""
    results = []

    if league == 'PremierLeague':
        pattern_league = 'http://www.bukmacherzy.com/liga_angielska/terminarz/'
    if league == 'PremieraDivision':
        pattern_league = 'http://www.bukmacherzy.com/liga_hiszpanska/terminarz/'
    if league == 'Ekstraklasa':
        pattern_league = 'http://www.bukmacherzy.com/ekstraklasa/terminarz/'

    rc = requests.get(pattern_league).content
    rc = re.findall('<div class="data">(.+)</div><div class="godzina">(.+)</div> .+ title="Typy (.+)\-(.+)"> .+ <strong>(.+?)</strong>', rc)  # TODO: fix pattern

    nr_match = 1

    for data in rc:
        result = {
            'nr_match': nr_match,
            'ft': data[2],
            'fts': int(data[4][0]),
            'st': data[3],
            'sts': int(data[4][2]),
            'md': parser.parse(data[0] + ' ' + data[1]),
        }
        results.append(result)

        nr_match += 1

    return results
