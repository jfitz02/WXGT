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

class Overall_Leaderboard:

    def __init__(self,master,colour):
        self.master = master
        self.colour = colour
        self.edition = {"Gold":"CHAMPIONS", "Green":"SF", "Purple":"UNI", "Yellow":"POSTUNI", "Blue":"QF"}
        self.bg_colours = {"Red":"#AA0000", "Gold":"#FFFFFF", "Green":"#2CB322", "Purple":"#8F06A1", "Yellow":"#E4ED42", "Blue":"#12C5E0"}
        self.draw_window()

    def takeSecond(self,elem):
        return elem[1]

    def takeThird(self,elem):
        return elem[2]

    def takeFourth(self,elem):
        return elem[3]

    def takeFifth(self,elem):
        return elem[4]

    def draw_window(self):
        self.master.configure(bg=self.bg_colours[self.colour])
        Label(self.master, text="Pos",bg=self.bg_colours[self.colour],width=5).grid(row=0, column=0)
        Label(self.master, text="Name",bg=self.bg_colours[self.colour],width=25).grid(row=0, column=1)
        Label(self.master, text="Points",bg=self.bg_colours[self.colour],width=7).grid(row=0, column=2)
        Label(self.master, text="Golds",bg=self.bg_colours[self.colour],width=5).grid(row=0, column=3)
        Label(self.master, text="Silvers",bg=self.bg_colours[self.colour],width=5).grid(row=0, column=4)
        Label(self.master, text="Bronzes",bg=self.bg_colours[self.colour],width=5).grid(row=0, column=5)
        for i in range(0,8):
            Label(self.master, text="",bg=self.bg_colours[self.colour],width=5).grid(row=(i*2)+1, column=0)
        Label(self.master, text="",bg=self.bg_colours[self.colour],width=5).grid(row=19, column=0)
        Label(self.master, text="1st",bg="#FFD700",width=5).grid(row=2, column=0)
        Label(self.master, text="2nd",bg="#C0C0C0",width=5).grid(row=4, column=0)
        Label(self.master, text="3rd",bg="#CD7F32",width=5).grid(row=6, column=0)
        Label(self.master, text="4th",bg=self.bg_colours[self.colour],width=5).grid(row=8, column=0)
        Label(self.master, text="5th",bg=self.bg_colours[self.colour],width=5).grid(row=10, column=0)
        Label(self.master, text="6th",bg=self.bg_colours[self.colour],width=5).grid(row=12, column=0)
        Label(self.master, text="7th",bg=self.bg_colours[self.colour],width=5).grid(row=14, column=0)
        Label(self.master, text="8th",bg=self.bg_colours[self.colour],width=5).grid(row=16, column=0)
        players_data  = self.get_overall_leaderboard(self.edition[self.colour])
        players_data  = sorted(players_data, key=self.takeFifth, reverse = True)
        players_data  = sorted(players_data, key=self.takeFourth, reverse = True)
        players_data  = sorted(players_data, key=self.takeThird, reverse = True)
        players_data  = sorted(players_data, key=self.takeSecond, reverse = True)
        print(players_data)
        for i in range(0,8):
            for j in range(0,len(players_data[i])):
                if i==0:
                    background = "#FFD700"
                elif i==1:
                    background = "#C0C0C0"
                elif i==2:
                    background = "#CD7F32"
                else:
                    background = self.bg_colours[self.colour]
                if j==0:
                    Label(self.master, text="",bg=background,width=25).grid(row=(i*2)+2, column=j+1)
                elif j==1:
                    Label(self.master, text="",bg=background,width=7).grid(row=(i*2)+2, column=j+1)
                else:
                    Label(self.master, text="",bg=background,width=5).grid(row=(i*2)+2, column=j+1)
                Label(self.master, text=players_data[i][j], bg=background).grid(row=(i*2)+2, column=j+1)


    def get_overall_leaderboard(self,SessionType):
        db = sql.connect("WXGT.db")
        c = db.cursor()

        c.execute('''SELECT SessionID FROM Session WHERE SessionType = "{}"'''.format(SessionType))

        data = c.fetchall()
        players = []
        scores = []
        golds = []
        silvers = []
        bronzes = []

        for session in data:
            session = session[0]
            c.execute('''SELECT PlayerName, Score, Golds, Silvers, Bronzes FROM SessionScores WHERE SessionID = {}'''.format(session))
            all_scores = c.fetchall()

            for score in all_scores:
                if score[0] not in players:
                    players.append(score[0])
                    scores.append(score[1])
                    golds.append(score[2])
                    silvers.append(score[3])
                    bronzes.append(score[4])
                else:
                    i = players.index(score[0])
                    scores[i] += score[1]
                    golds[i] += score[2]
                    silvers[i] += score[3]
                    bronzes[i] += score[4]

        data = []
        for i in range(len(players)):
            data.append((players[i], scores[i], golds[i], silvers[i], bronzes[i]))

        return data

def create_window(master, colour):
    window = Overall_Leaderboard(master, colour)
    master.mainloop()


    



                    
