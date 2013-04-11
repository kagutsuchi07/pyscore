import requests
import re
import torndb

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


def getFixtures(league, fpr):
    """Returns all fixtures."""
    fixtures = []

    if league == 'PremierLeague':
        pattern_league = 'http://www.bukmacherzy.com/liga_angielska/terminarz/'
    if league == 'PremieraDivision':
        pattern_league = 'http://www.bukmacherzy.com/liga_hiszpanska/terminarz/'
    if league == 'Ekstraklasa':
        pattern_league = 'http://www.bukmacherzy.com/ekstraklasa/terminarz/'
        
    rc = requests.get(pattern_league).content
    pattern_create = re.findall('<div class="data">(.+)</div><div class="godzina">(.+)</div> .+ title="Typy (.+)\-(.+)">', rc)

    nr_round = 0
    nr_match = 1

    for value in pattern_create:
        if (nr_match - 1) % fpr == 0:
            nr_round += 1

        match_date = parse(value[0] + ' ' + value[1])

        fixture = {
            'nr_match': nr_match,
            'nr_round': nr_round,
            'ft': value[2],
            'st': value[3],
            'md': match_date,
        }
        fixtures.append(fixture)

        nr_match += 1

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
    pattern_update = re.findall('<div class="data">(.+)</div><div class="godzina">(.+)</div> .+ title="Typy (.+)\-(.+)"> .+ <strong>(.+?)</strong>', rc)
 
    nr_match = 1

    for value in pattern_update:

        match_date = parse(value[0] + ' ' + value[1])

        result = {
            'nr_match': nr_match,
            'ft': value[2],
            'fts': int(value[4][0]),
            'st': value[3],
            'sts': int(value[4][2]),
            'md': match_date,
        }
        results.append(result)
 
        nr_match += 1
 
    return results
