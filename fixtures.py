import requests
import re
import torndb

# DATABASE VALUES (Fixture, Round, First_Team, FT_Score, Second_Team, ST_Score, Date(y-m-d 16:00:00)


def insert_values():

    db = torndb.Connection('db4free.net', 'pyscore', 'login', 'pwd')
    rc = requests.get('http://www.bukmacherzy.com/liga_angielska/terminarz/').content
    pattern_create = re.findall('<div class="data">(.+)</div><div class="godzina">(.+)</div> .+ title="Typy .+\-.+">(.+) \- (.+?)</a>', rc)

    nr_round = 0
    nr_match = 1

    for value in pattern_create:
        FT = value[2]
        ST = value[3]

        if (nr_match - 1) % 10 == 0:
            nr_round += 1

        db.execute("INSERT INTO PremierLeague VALUES(%s, %s, %s, NULL, %s, NULL, NULL)", nr_match, nr_round, FT, ST)
        print nr_match, nr_round, FT, 'NULL', ST, 'NULL', 'NULL'

        nr_match += 1
    db.close()


def update_values():

    db = torndb.Connection('db4free.net', 'pyscore', 'login', 'pwd')
    rc = requests.get('http://www.bukmacherzy.com/liga_angielska/terminarz/').content
    pattern_update = re.findall('<div class="data">(.+)</div><div class="godzina">(.+)</div> .+ title="Typy .+\-.+">(.+) <strong>(.+?)</strong>(.+?)</a>', rc)

    nr_round = 0
    nr_match = 1

    for value in pattern_update:
        score = value[3]

        FT = value[2]
        FTS = score[0]
        ST = value[4]
        STS = score[2]

        if (nr_match - 1) % 10 == 0:
            nr_round += 1

        db_check = db.query("SELECT Fixture, FT_Score, ST_Score FROM PremierLeague WHERE 1")
        db_values = db_check[nr_match]

        dbFTS = db_values['FT_Score']
        dbSTS = db_values['ST_Score']

        if dbFTS == FTS and dbSTS == STS:
            print 'OK'
        else:
            db.execute("UPDATE PremierLeague SET FT_Score = %s, ST_Score = %s WHERE First_Team = %s AND Second_Team = %s", FTS, STS, FT, ST)
            print 'Fixture: ', nr_match, "First Team Score: ", FTS, 'Second Team Score: ', STS, '...UPDATED'

        nr_match += 1
    db.close()
