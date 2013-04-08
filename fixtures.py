import requests
import re
import torndb

db = torndb.Connection('db4free.net', 'pyscore', 'login', 'haslo')
rc = requests.get('http://www.bukmacherzy.com/liga_angielska/terminarz/').content
pattern = re.findall('<div class="data">(.+)</div><div class="godzina">(.+)</div> .+ title="Typy .+\-.+">(.+) <strong>(.+?)</strong>(.+?)</a>', rc)

# VALUES(Fixture, Round, First_Team, FT_Score, Second_Team, ST_Score, Match_Date)

def insert_values():
    
    nr_round = 0
    nr_match = 1

    for value in pattern_create:
        FT = value[2]
        ST = value[3]

        if (nr_match - 1) % 10 == 0:
            nr_round += 1

        db.execute("INSERT INTO PremierLeague VALUES(%s, %s, %s, NULL, %s, NULL, NULL)", nr_match, nr_round, FT, ST)

        nr_match +=1
    db.close()
    
def update_values():
    
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
        
        db.execute("UPDATE PremierLeague SET FT_Score = %s, ST_Score = %s", FTS, STS)

        nr_match += 1
 
    db.close()
