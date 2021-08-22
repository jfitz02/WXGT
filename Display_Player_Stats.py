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

class Display_Player_Stats:

    def __init__(self,master,colour):
        self.master = master
        self.colour = colour
        self.error = False
        self.edition = {"Gold":"CHAMPIONS", "Green":"SF", "Purple":"UNI", "Yellow":"POSTUNI", "Blue":"QF"}
        self.bg_colours = {"Red":"#AA0000", "Gold":"#FFFFFF", "Green":"#2CB322", "Purple":"#8F06A1", "Yellow":"#E4ED42", "Blue":"#12C5E0"}
        self.draw_window()

    def draw_window(self):
        self.master.configure(bg=self.bg_colours[self.colour])
        self.master.title("Competitor Stats")
        Label(self.master, text=" ",bg=self.bg_colours[self.colour],width=5).grid(row=0, column=0)
        Label(self.master, text=" ",bg=self.bg_colours[self.colour],width=5).grid(row=0, column=2)
        self.Label = Label(self.master, text="Competitor",bg=self.bg_colours[self.colour])
        self.Label.grid(row=0, column=1)
        self.Name=StringVar()
        Label(self.master, text=" ",bg=self.bg_colours[self.colour],width=5).grid(row=1, column=1)
        self.Entry = Entry(self.master, textvariable = self.Name, width=25)
        self.Entry.grid(row=2, column=1)
        Label(self.master, text=" ",bg=self.bg_colours[self.colour],width=5).grid(row=3, column=1)
        self.button = Button(self.master, text="Confirm",bg=self.bg_colours[self.colour], command=self.continue_window)
        self.button.grid(row=4, column=1)

    def continue_window(self):
        print(self.Name.get())
        exists = self.check_players(self.Name.get(), self.edition[self.colour])
        if exists == True:
            self.Label_1 = Label(self.master, text="Name not in database!",bg='#AA0000',width=25)
            self.Label_1.grid(row=3, column=1)
            self.error = True
        else:
            if self.error == True:
                self.Label_1.destroy()
            self.button.destroy()
            self.Entry.destroy()
            Stats = self.get_session_for_player(self.edition[self.colour],self.Name.get())
            Label(self.master, text=self.Name.get(),bg=self.bg_colours[self.colour],width=25).grid(row=0, column=1)
            Label(self.master, text=" ",bg=self.bg_colours[self.colour],width=5).grid(row=1, column=0)
            Titles = ["Total Points:","Highest Point Session:","Lowest Point Session:","Season Wins:","Season Top 4s:","Season Lasts:","Total Golds:","Total Silvers:","Total Bronzes:"]
            for i in range(0,len(Titles)):
                Label(self.master, text=Titles[i],bg=self.bg_colours[self.colour],width=25).grid(row=(i*2)+2, column=0)
                Label(self.master, text=Stats[i],bg=self.bg_colours[self.colour],width=25).grid(row=(i*2)+2, column=2)
                Label(self.master, text="",bg=self.bg_colours[self.colour],width=25).grid(row=(i*2)+3, column=0)
                
            

    def check_players(self, name, edition):
        db = sql.connect("WXGT.db")
        c = db.cursor()

        c.execute('''SELECT PlayerName FROM SessionScores, Session WHERE PlayerName = "{}" AND Session.SessionType = "{}" AND Session.SessionID = SessionScores.SessionID'''.format(name, edition))

        data = c.fetchall()

        db.commit()

        if len(data) == 0:
            return True
        return False


    def get_session_for_player(self,SessionType, Player):            #will need self in class.
        #### returns the following. [Points,Highest point session, Lowest point Session, Season wins, Season Top 4, Season Last, Golds, Silvers, Bronze]
        db = sql.connect("WXGT.db")
        c = db.cursor()

        c.execute('''SELECT Score, Golds, Silvers, Bronzes, Session.SessionID FROM SessionScores, Session WHERE Session.SessionType = "{}" AND Session.SessionID = SessionScores.SessionID AND PlayerName = "{}"'''.format(SessionType, Player))

        data = c.fetchall()

        points = [data[i][0] for i in range(len(data))]
        total_points = sum(points)
        golds = sum([data[i][1] for i in range(len(data))])
        silvers = sum([data[i][2] for i in range(len(data))])
        bronzes = sum([data[i][3] for i in range(len(data))])


        max_points = max(points)
        min_points = min(points)

        c.execute('''SELECT SessionID FROM Session WHERE SessionType = "{}"'''.format(SessionType))

        data = c.fetchall()
        wins = 0
        fourths = 0
        lasts = 0
        for session in data:
            print(session)
            c.execute('''SELECT Score, PlayerName FROM SessionScores WHERE SessionID = {}'''.format(session[0]))
            players = c.fetchall()

            table = [(i, j) for i, j in players]

            table = sorted(table, reverse = True)
            print(table)

            if table[0][1] == Player:
                wins += 1
                fourths += 1
            elif table[7][1] == Player:
                lasts += 1

            elif table[1][1] == Player or table[2][1] == Player or table[3][1] == Player:
                fourths += 1



        return total_points,max_points, min_points, wins, fourths, lasts, golds, silvers, bronzes

def create_window(root, colour):
    window = Display_Player_Stats(root,colour)
    root.mainloop()

