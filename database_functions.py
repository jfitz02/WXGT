import sqlite3 as sql

def get_medals(SessionType, medal, one_session = False):
    db = sql.connect("WXGT.db")
    c = db.cursor()

    c.execute('''SELECT PlayerName FROM Players''')

    players = c.fetchall()

    highest_score = 0
    highest_player = None
    for player in players:
        player = player[0]
        c.execute('''SELECT {} FROM SessionScores, Session WHERE PlayerName = "{}" AND Session.SessionType = "{}" AND Session.SessionID = SessionScores.SessionID'''.format(medal, player, SessionType))
        data = c.fetchall()
        medals = 0
        if one_session == False:
            for session in data:
                medals += session[0]

            if medals > highest_score:
                highest_score = medals
                highest_player = player
        else:
            for session in data:
                medals = session[0]

                if medals >  highest_score:
                    highest_score = medals
                    highest_player = player

    return highest_score, highest_player














def lowest_point_total(SessionType):
    db = sql.connect("WXGT.db")
    c = db.cursor()

    c.execute('''SELECT PlayerName FROM Players''')

    players = c.fetchall()
    lowest = 200
    lowest_player = None
    for player in players:
        player = player[0]
        c.execute('''SELECT Score FROM SessionScores, Session WHERE PlayerName = "{}" AND Session.SessionType = "{}" AND Session.SessionID = SessionScores.SessionID'''.format(player, SessionType))
        data = c.fetchall()

        for session in data:
            if session[0]<lowest:
                lowest = session[0]
                lowest_player = player

    return lowest, lowest_player












def takeSecond(elem):
        return elem[1]

def takeThird(elem):
    return elem[2]

def takeFourth(elem):
    return elem[3]

def takeFifth(elem):
    return elem[4]

def lowest_fourth(SessionType):
    db = sql.connect("WXGT.db")
    c = db.cursor()

    c.execute('''SELECT SessionID FROM Session WHERE SessionType = "{}"'''.format(SessionType))

    sessions = c.fetchall()
    lowest = 200
    for session in sessions:
        session = session[0]
        c.execute('''SELECT PlayerName, Score, Golds, Silvers, Bronzes FROM SessionScores WHERE SessionID = {}'''.format(session))

        scores = c.fetchall()
        leaderboard= []
        for score in scores:
            leaderboard.append(score)

        leaderboard = sorted(leaderboard, key = takeFifth, reverse = True)
        leaderboard = sorted(leaderboard, key = takeFourth, reverse = True)
        leaderboard = sorted(leaderboard, key = takeThird, reverse = True)
        leaderboard = sorted(leaderboard, key = takeSecond, reverse = True)

        score = leaderboard[3][1]

        if score<lowest:
            lowest = score
            lowest_player = leaderboard[3][0]

    return lowest, lowest_player


def highest_fifth(SessionType):
    db = sql.connect("WXGT.db")
    c = db.cursor()

    c.execute('''SELECT SessionID FROM Session WHERE SessionType = "{}"'''.format(SessionType))

    sessions = c.fetchall()
    highest = 0

    for session in sessions:
        session = session[0]
        c.execute('''SELECT PlayerName, Score, Golds, Silvers, Bronzes FROM SessionScores WHERE SessionID = {}'''.format(session))

        scores = c.fetchall()
        leaderboard= []
        for score in scores:
            leaderboard.append(score)

        leaderboard = sorted(leaderboard, key = takeFifth, reverse = True)
        leaderboard = sorted(leaderboard, key = takeFourth, reverse = True)
        leaderboard = sorted(leaderboard, key = takeThird, reverse = True)
        leaderboard = sorted(leaderboard, key = takeSecond, reverse = True)

        score = leaderboard[4][1]

        if score>highest:
            highest = score
            highest_player = leaderboard[4][0]

    return highest, highest_player
