import tkinter
from tkinter import *
from functools import partial
import ID_fetcher as idf
import sqlite3 as sql

#red = #AA0000
#gold = #FFFFFF
#green = #2CB322
#purple = #8F06A1
#yellow = #E4ED42
#blue = #12C5E0

class Overall_Stats:

    def __init__(self,master,colour):
        self.master = master
        self.colour = colour
        self.edition = {"Gold":"CHAMPIONS", "Green":"SF", "Purple":"UNI", "Yellow":"POSTUNI", "Blue":"QF"}
        self.bg_colours = {"Red":"#AA0000", "Gold":"#FFFFFF", "Green":"#2CB322", "Purple":"#8F06A1", "Yellow":"#E4ED42", "Blue":"#12C5E0"}
        self.draw_window()

    def draw_window(self):
        self.master.configure(bg=self.bg_colours[self.colour])
        self.master.title("Overall Stats")
        Label(self.master, text=" ",bg=self.bg_colours[self.colour],width=5).grid(row=0, column=0)
        Stats = [self.get_medals(self.edition[self.colour],"Golds"),self.get_medals(self.edition[self.colour],"Golds",True),self.get_medals(self.edition[self.colour],"Silvers"),self.get_medals(self.edition[self.colour],"Silvers",True),self.get_medals(self.edition[self.colour],"Bronzes"),self.get_medals(self.edition[self.colour],"Bronzes",True),self.get_medals(self.edition[self.colour],"Score",True),self.lowest_point_total(self.edition[self.colour]),self.lowest_fourth(self.edition[self.colour]),self.highest_fifth(self.edition[self.colour])]
        Titles = ["Highest Total Golds:","Highest Golds in a Session:","Highest Total Silvers:","Highest Silvers in a Session:","Highest Total Bronzes:","Highest Bronzes in a session:","Highest point total in a single session:","Lowest point total in a single session:","Lowest point total to finish 4th:","Highest point total to finish 5th:"]
        for i in range(0,len(Titles)):
            Score,Player = Stats[i]
            Label(self.master, text=Titles[i],bg=self.bg_colours[self.colour],width=30).grid(row=(i*2)+1, column=0)
            Label(self.master, text="",bg=self.bg_colours[self.colour],width=3).grid(row=(i*2)+1, column=1)
            Label(self.master, text=Player,bg=self.bg_colours[self.colour],width=25).grid(row=(i*2)+1, column=2)
            Label(self.master, text="-",bg=self.bg_colours[self.colour],width=5).grid(row=(i*2)+1, column=3)
            Label(self.master, text=Score,bg=self.bg_colours[self.colour],width=8).grid(row=(i*2)+1, column=4)
            Label(self.master, text="",bg=self.bg_colours[self.colour],width=25).grid(row=(i*2)+2, column=0)
            
        


    def get_medals(self,SessionType, medal, one_session = False):
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


    def lowest_point_total(self,SessionType):
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


    def takeSecond(self,elem):
            return elem[1]

    def takeThird(self,elem):
        return elem[2]

    def takeFourth(self,elem):
        return elem[3]

    def takeFifth(self,elem):
        return elem[4]

    def lowest_fourth(self,SessionType):
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

            leaderboard = sorted(leaderboard, key = self.takeFifth, reverse = True)
            leaderboard = sorted(leaderboard, key = self.takeFourth, reverse = True)
            leaderboard = sorted(leaderboard, key = self.takeThird, reverse = True)
            leaderboard = sorted(leaderboard, key = self.takeSecond, reverse = True)

            score = leaderboard[3][1]

            if score<lowest:
                lowest = score
                lowest_player = leaderboard[3][0]

        return lowest, lowest_player


    def highest_fifth(self,SessionType):
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

            leaderboard = sorted(leaderboard, key = self.takeFifth, reverse = True)
            leaderboard = sorted(leaderboard, key = self.takeFourth, reverse = True)
            leaderboard = sorted(leaderboard, key = self.takeThird, reverse = True)
            leaderboard = sorted(leaderboard, key = self.takeSecond, reverse = True)

            score = leaderboard[4][1]

            if score>highest:
                highest = score
                highest_player = leaderboard[4][0]

        return highest, highest_player

def create_window(root, colour):
    window = Overall_Stats(root,colour)
    root.mainloop()
