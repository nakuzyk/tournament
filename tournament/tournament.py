#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect(database_name = "tournament"):
    """Connect to the PostgreSQL database.
    Returns a database connection and a cursor.
    """
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Error.")

def registerPlayer(name_player):
    """Adds a player to the tournament by putting an entry in the database. 
	The database should assign an ID number to the player.
	Different players may have the same names but will receive different ID numbers."""
    db, cursor = connect()

    query = "INSERT INTO players (name_player) VALUES (%s)"
    params = (name_player,)
    cursor.execute(query, params)

    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()

    query = "SELECT count(*) FROM players"
    cursor.execute(query)
    row = cursor.fetchone()

    db.close()

    players_count = row[0]

    return players_count
	
def deletePlayers():
    """Clear out all the player records from the database."""
    db, cursor = connect()

    query = "DELETE FROM players"
    cursor.execute(query)

    db.commit()
    db.close()
	
def reportMatch(winner_match, loser_match):
    """Stores the outcome of a single match between two players in the database."""
    db, cursor = connect()

    query = ("INSERT INTO matches(winner_match, loser_match) VALUES (%s, %s)")
    params = (winner_match, loser_match,)
    cursor.execute(query, params)

    db.commit()
    db.close()
	
def deleteMatches():
    """Clear out all the match records from the database."""
    db, cursor = connect()

    query = "DELETE FROM matches"
    cursor.execute(query)

    db.commit()
    db.close()

def playerStandings():
    """Returns a list of (id, name, wins, matches) for each player, sorted by the number of wins each player has."""
    standings = []

    db, cursor = connect()

    query = ("SELECT win_rank.id, "
             "       win_rank.name, "
             "       win_rank.wins, "
             "       COALESCE(loss_count.losses, 0) AS losses "
             "FROM "
             "       (SELECT players.id_player AS id, "
             "               players.name_player AS name, "
             "               COALESCE(win_count.wins, 0) AS wins "
             "        FROM "
             "               (SELECT winner_match, "
             "                       COUNT(winner_match) AS wins "
             "                       FROM matches "
             "                       GROUP BY winner_match) "
             "                AS win_count "
             "        FULL JOIN "
             "                players "
             "        ON players.id_player = win_count.winner_match) "
             "        AS win_rank "
             "FULL JOIN "
             "       (SELECT loser_match, "
             "               COUNT(loser_match) AS losses "
             "               FROM matches "
             "               GROUP BY loser_match) "
             "        AS loss_count "
             "        ON win_rank.id = loss_count.loser_match "
             "        ORDER BY win_rank.wins DESC")
    cursor.execute(query)
    rows = cursor.fetchall()

    db.close()

    for row in rows:
        matches_count = int(row[2]) + int(row[3])
        player_tuple = (row[0], row[1], int(row[2]), matches_count)
        standings.append(player_tuple)
    return standings

def swissPairings():
    """Given the existing set of registered players and the matches they have played, 
	generates and returns a list of pairings according to the Swiss system. Each pairing 
	is a tuple (id1, name1, id2, name2), giving the ID and name of the paired players. 
	For instance, if there are eight registered players, this function should return four pairings. 
	This function should use playerStandings to find the ranking of players."""
    pairings = []
    standings = playerStandings()
    for i in range(0, len(standings), 2):
        id1 = standings[i][0]
        name1 = standings[i][1]
        id2 = standings[i+1][0]
        name2 = standings[i+1][1]
        pair = (id1, name1, id2, name2)
        pairings.append(pair)
    return pairings
