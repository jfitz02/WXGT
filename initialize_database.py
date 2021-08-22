import sqlite3 as sql

def create_database():
    db = sql.connect("WXGT.db")
    c = db.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS Players(PlayerName TEXT PRIMARY KEY)''')

    c.execute('''CREATE TABLE IF NOT EXISTS Session(SessionID INTEGER PRIMARY KEY,
                                                                                            SessionType TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS Games(GameID INT PRIMARY KEY,
                                                                                            Name TEXT,
                                                                                            Type TEXT,
                                                                                            Console TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS SessionScores(PlayerName TEXT,
                                                                                                        SessionID INTEGER,
                                                                                                        Score INTEGER,
                                                                                                        Golds INTEGER,
                                                                                                        Silvers INTEGER,
                                                                                                        Bronzes INTEGER,
                                                                                                        FOREIGN KEY(SessionID) REFERENCES Session(SessionID),
                                                                                                        FOREIGN KEY(PlayerName) REFERENCES Players(PlayerName),
                                                                                                        PRIMARY KEY(PlayerName, SessionID))''')


create_database()
