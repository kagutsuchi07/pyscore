import requests
import re
import torndb

# DATABASE VALUES (Fixture, Round, First_Team, FT_Score, Second_Team, ST_Score, Date(y-m-d 16:00:00)


# === DB
def dbInsertFixtures(fixtures):
    """Inserts all fixtures into database.

    :param fixtures: List of fixtures.
    """
    db = torndb.Connection('db4free.net', 'pyscore', 'login', 'pwd')

    for fixture in fixtures:
        db.execute("INSERT INTO PremierLeague VALUES(%s, %s, %s, NULL, %s, NULL, NULL)", fixture['nr_match'], fixture['nr_round'], fixture['ft'], fixture['st'])
        print fixture['nr_match'], fixture['nr_round'], fixture['ft'], 'NULL', fixture['st'], 'NULL', 'NULL'

    db.close()


def dbUpdateResults(results):
    """Updates all results in database.

    :param results: List of results.
    """
    db = torndb.Connection('db4free.net', 'pyscore', 'login', 'pwd')

    for result in results:
        db_values = db.get("SELECT Fixture, FT_Score, ST_Score FROM PremierLeague WHERE Fixture=%s", result['nr_match'])
        db_fts = db_values['FT_Score']
        db_sts = db_values['ST_Score']

        if db_fts == result['fts'] and db_sts == result['sts']:
            print 'OK'
        else:
            db.execute("UPDATE PremierLeague SET FT_Score = %s, ST_Score = %s WHERE First_Team = %s AND Second_Team = %s", result['fts'], result['sts'], result['ft'], result['st'])

        print 'Fixture: ', result['nr_match'], "First Team Score: ", result['fts'], 'Second Team Score: ', result['sts'], '...UPDATED'

    db.close()
# === DB end


def getFixtures():
    """Returns all fixtures."""
    fixtures = []
    rc = requests.get('http://www.bukmacherzy.com/liga_angielska/terminarz/').content
    pattern_create = re.findall('</div> .+ title="Typy (.+)\-(.+)">', rc)

    nr_round = 0
    nr_match = 1

    for value in pattern_create:
        if (nr_match - 1) % 10 == 0:
            nr_round += 1

        fixture = {
            'nr_match': nr_match,
            'nr_round': nr_round,
            'ft': value[0],
            'st': value[1],
        }
        fixtures.append(fixture)

        nr_match += 1

    return fixtures


def getResults():
    """Returns all results."""
    results = []
    rc = requests.get('http://www.bukmacherzy.com/liga_angielska/terminarz/').content
    pattern_update = re.findall('<div class="data">(.+)</div><div class="godzina">(.+)</div> .+ title="Typy .+\-.+">(.+) <strong>(.+?)</strong>(.+?)</a>', rc)

    nr_round = 0
    nr_match = 1

    for value in pattern_update:
        if (nr_match - 1) % 10 == 0:
            nr_round += 1

        result = {
            'nr_match': nr_match,
            'ft': value[2],
            'fts': int(value[3][0]),
            'st': value[4],
            'sts': int(value[3][2]),
        }
        results.append(result)

        nr_match += 1

    return results
