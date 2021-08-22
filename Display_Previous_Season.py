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

class Display_Previous_Season:

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
        self.master.title("Choose Season")
        self.Amount = self.get_all_seasons(self.edition[self.colour])
        Seasons = []
        for i in range(0,len(self.Amount)):
            Seasons.append(i+1)
        self.Selected_Season = StringVar(self.master)
        self.Selected_Season.set(1)
        Label(self.master, text=" ",bg=self.bg_colours[self.colour],width=5).grid(row=0, column=0)
        Label(self.master, text=" ",bg=self.bg_colours[self.colour],width=5).grid(row=0, column=2)
        Label(self.master, text=" ",bg=self.bg_colours[self.colour],width=5).grid(row=3, column=1)
        self.initial_label = Label(self.master, text="Season",bg=self.bg_colours[self.colour])
        self.initial_label.grid(row=1, column=1)
        self.initial_option = OptionMenu(self.master,self.Selected_Season, *Seasons)
        self.initial_option.grid(row=2,column=1)
        self.initial_button = Button(self.master, text="Confirm",bg=self.bg_colours[self.colour], command=partial(self.continue_draw))
        self.initial_button.grid(row=4, column=1)

    def continue_draw(self):
        print(self.Selected_Season.get())
        print(self.Amount[int(self.Selected_Season.get())-1][0])
        self.initial_label.destroy()
        self.initial_option.destroy()
        self.initial_button.destroy()
        players_data = self.get_previous_season(self.Amount[int(self.Selected_Season.get())-1][0])
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
        players_data  = sorted(players_data, key=self.takeFifth, reverse = True)
        players_data  = sorted(players_data, key=self.takeFourth, reverse = True)
        players_data  = sorted(players_data, key=self.takeThird, reverse = True)
        players_data  = sorted(players_data, key=self.takeSecond, reverse = True)
        print(players_data)
        for i, player in enumerate(players_data):
            for j in range(0,len(player)):
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
                Label(self.master, text=player[j], bg=background).grid(row=(i*2)+2, column=j+1)

    def get_all_seasons(self,SessionType):      #gets all session ID's in the following order
                                                                    # season1, season 2, season 3...
                                                                    #this could be used in a drop down menu to select the session you want
        db = sql.connect("WXGT.db")
        c = db.cursor()

        c.execute('''SELECT SessionID FROM Session WHERE SessionType = "{}"'''.format(SessionType))

        sessions = c.fetchall()
        db.commit()

        return sessions

    def get_previous_season(self,session):  #pass into the sessionID of the selected session
        db = sql.connect("WXGT.db")
        c = db.cursor()

        c.execute('''SELECT PlayerName, Score, Golds, Silvers, Bronzes FROM SessionScores WHERE SessionID = "{}"'''.format(session))
        
        data = c.fetchall()

        return data             #returns the scores as for a normal leaderboard. So needs sorting
        
def create_window(root, colour):
    window = Display_Previous_Season(root,colour)
    root.mainloop()


                    
