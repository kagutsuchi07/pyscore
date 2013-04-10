import torndb

def new_tournament(tournament_name):
    """
    Creates new table where will be kept players and their points
    WORK IN PROGRESS
    """

    db = torndb.Connection('db4free.net', 'pyscore', 'login', 'pwd')

    create_tournament = db.execute("IF (EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'pyscore' AND  TABLE_NAME = '%s')) \
                                    BEGIN CREATE TABLE %s (ID TINYINT(2) UNSIGNED AUTO_INCREMENT PRIMARY KEY, Player VARCHAR(20), Points SMALLINT(3) UNSIGNED NULL) END", tournament_name)
    db.close()
    print "Created new tournment ", tournment_name


def new_player(player_name):
    """
    Creates new table where will be kept scores
    WORK IN PROGRESS
    """

    db = torndb.Connection('db4free.net', 'pyscore', 'login', 'pwd')

    create_player = db.execute("IF (EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'pyscore' AND  TABLE_NAME = '%s')) \
                                BEGIN CREATE TABLE %s (ID SMALLINT(4) UNSIGNED AUTO_INCREMENT PRIMARY KEY, League VARCHAR(20) INDEX, Home_Team VARCHAR(20) INDEX, \
                                HT_Score TINYINT(2) UNSIGNED, Away_Team VARCHAR(20) INDEX, AT_Score TINYINT(2) UNSIGNED, Match_Date DATETIME) END", player_name)
    db.close()
    print "Created new player ", player_name


def player_to_tournament(player_name, tournament_name):
    """Add player to tournament"""

    db = torndb.Connection('db4free.net', 'pyscore', 'login', 'pwd')

    db.execute("INSERT INTO %s (Player) VALUES %s", tournament_name, player_name)
    db.close()
    print "Added ", player_name, 'into ', tournament_name

    
def check_score(player_name, league_name):
    """Check if all user typed scores are equal to actual scores and returns user points"""

    db = torndb.Connection('db4free.net', 'pyscore', 'login', 'pwd')

    match = db.query("SELECT First_Team, Second_Team FROM player_name")

    player_points = 0

    for teams in match:

        home = match['First_Team']
        away = match['Second_Team']

        player_score = db.get("SELECT FT_Score, ST_Score FROM player_name WHERE League =%s First_Team =%s AND Second_Team = %s", league_name, home, away)
        actual_score = db.get("SELECT FT_Score, ST_Score FROM league_name WHERE First_Team =%s AND Second_Team = %s", home, away)

        p_fts = player_score['FT_Score']
        p_sts = player_score['ST_Score']

        fts = actual_score['FT_Score']
        sts = actual_score['ST_Score']

        if (p_fts == fts and p_sts == sts):
            player_points += 3
            print home, away, 'Awesome! You got score right! 3 points'
        elif (p_fts > p_sts and fts > sts):
            player_points += 1
            print home, away, 'You got the winner right. 1 point'
        elif (p_fts < p_sts and fts < sts):
            player_points += 1
            print home, away, 'You got the winner right. 1 point'
        elif (pfts == p_sts and fts == sts):
            player_points += 1
            print home, away, 'You got the draw right. 1 point'
    db.close()    
    return player_points


def update_points(player_name, tournament_name):
    """Updates player points in tournament table"""
    
    check_score(player_name)
    db = torndb.Connection('db4free.net', 'pyscore', 'login', 'pwd')

    db.execute("UPDATE %s SET Points = %s WHERE Player = %s", tournment_name, player_points, player_name)
    db.close()
    print "Updated player ", player_name, "points: ", player_points
