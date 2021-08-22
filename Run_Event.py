#Tom Stuart
#02.06.2020
#WXGT
import tkinter
import random
from tkinter import *
from functools import partial
import sqlite3 as sql

#red = #AA0000
#gold = #FFFFFF
#green = #2CB322
#purple = #8F06A1
#yellow = #E4ED42
#blue = #12C5E0

class Numbers:

    def __init__(self,master,colour,names,to_final, sessID, prev):
        self.master = master
        self.prev = prev
        self.colour = colour
        self.names = names
        self.sessID = sessID
        self.to_final = to_final
        self.draw_window()

    def close(self):
        
        self.prev.close()

    def draw_window(self):
        self.master.configure(bg=self.colour)
        self.master.title("Number ranking")
        Label(self.master, text="Name",bg=self.colour,width=25).grid(row=0, column=0)
        Label(self.master, text="Score",bg=self.colour,width=25).grid(row=0, column=1)
        Label(self.master, text="",bg=self.colour,width=25).grid(row=1, column=0)
        Label(self.master, text="",bg=self.colour,width=25).grid(row=1, column=1)
        self.Scores = [StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar()]
        for i in range(0,8):
            Label(self.master, text=self.names[i],bg=self.colour,width=25).grid(row=(i*2)+2, column=0)
            Label(self.master, text="",bg=self.colour,width=25).grid(row=(i*2)+3, column=0)
            Label(self.master, text="",bg=self.colour,width=25).grid(row=(i*2)+3, column=1)
            Entry(self.master, textvariable = self.Scores[i], width=25).grid(row=(i*2)+2, column=1)
        Button(self.master, text="Confirm",bg=self.colour, command=partial(self.error_check)).grid(row=18, column=1)
        Button(self.master, text="Get Pairings",bg=self.colour, command=partial(self.pair)).grid(row=18, column=0)

    def takeSecond(self,elem):
        return elem[1]

    def error_check(self):
        confirmed_scores = ["","","","","","","",""]
        accepted = True
        for i in range(0,8):
            try:
                confirmed_scores[i] = (self.names[i],float(self.Scores[i].get()))
                Label(self.master, text="",bg=self.colour,width=25).grid(row=(i*2)+3, column=2)
            except:
                Label(self.master, text="Not a valid input",bg="#AA0000",width=25).grid(row=(i*2)+3, column=2)
                accepted = False
        if accepted == True:
            if self.to_final == True:
                table = sorted(confirmed_scores, key=self.takeSecond, reverse = False)
            else:
                table = sorted(confirmed_scores, key=self.takeSecond, reverse = True)
            newlevel = Toplevel(self.master)
            win = Table(newlevel, self.colour, self.names, self.to_final, table, self.sessID, self.prev)

    def pair(self):
        newlevel = Toplevel(self.master)
        win = pairing(newlevel,self.colour,self.names,False)
                
class Table:

    def __init__(self,master,colour,names,to_final,table, sessID, prev):
        self.master = master
        self.prev = prev
        self.colour = colour
        self.names = names
        self.sessID = sessID
        self.to_final = to_final
        self.table = table
        self.draw_window()

    def close(self):
        self.prev.close()

    def draw_window(self):
        self.master.configure(bg=self.colour)
        self.master.title("Positions")
        Label(self.master, text="Pos",bg=self.colour,width=5).grid(row=0, column=0)
        Label(self.master, text="Name",bg=self.colour,width=25).grid(row=0, column=1)
        Label(self.master, text="Score",bg=self.colour,width=25).grid(row=0, column=2)
        Label(self.master, text="",bg=self.colour,width=25).grid(row=1, column=0)
        Label(self.master, text="1st",bg=self.colour,width=5).grid(row=2, column=0)
        Label(self.master, text="2nd",bg=self.colour,width=5).grid(row=4, column=0)
        Label(self.master, text="3rd",bg=self.colour,width=5).grid(row=6, column=0)
        Label(self.master, text="4th",bg=self.colour,width=5).grid(row=8, column=0)
        Label(self.master, text="5th",bg=self.colour,width=5).grid(row=10, column=0)
        Label(self.master, text="6th",bg=self.colour,width=5).grid(row=12, column=0)
        Label(self.master, text="7th",bg=self.colour,width=5).grid(row=14, column=0)
        Label(self.master, text="8th",bg=self.colour,width=5).grid(row=16, column=0)
        for i in range(0,8):
            Label(self.master, text=self.table[i][0],bg=self.colour,width=25).grid(row=(i*2)+2, column=1)
            Label(self.master, text=self.table[i][1],bg=self.colour,width=25).grid(row=(i*2)+2, column=2)
            Label(self.master, text="",bg=self.colour,width=5).grid(row=(i*2)+3, column=1)
        Button(self.master, text="Confirm",bg=self.colour, command=partial(self.next_step)).grid(row=18, column=1)

    def next_step(self):
        if self.to_final == True:
            newlevel = Toplevel(self.master)
            win = Placement(newlevel,self.colour,[self.table[0][0],self.table[1][0],self.table[2][0],self.table[3][0]], self.sessID, self.prev)
        else:
            self.database_input()
            self.master.destroy()

    def database_input(self):
        db = sql.connect("WXGT.db")
        c = db.cursor()
        medal = {0:"Golds",1:"Silvers",2:"Bronzes"}
        for i in range(3):
            c.execute('''SELECT {} FROM SessionScores WHERE SessionID = {} AND PlayerName = "{}"'''.format(medal[i], self.sessID, self.table[i][0]))
            medals = c.fetchall()[0][0]
            print(medals)
            c.execute('''UPDATE SessionScores SET {} = {} WHERE SessionID = {} AND PlayerName = "{}" '''.format(medal[i], medals+1, self.sessID, self.table[i][0]))

            c.execute('''SELECT Score FROM SessionScores WHERE SessionID = {} AND PlayerName = "{}"'''.format(self.sessID, self.table[i][0]))
            score = c.fetchall()[0][0]

            c.execute('''UPDATE SessionScores SET Score={} wHERE SessionID = {} AND PlayerName = "{}"'''.format(score+4-i, self.sessID, self.table[i][0]))

        c.execute('''SELECT Score FROM SessionScores WHERE SessionID = {} AND PlayerName = "{}"'''.format(self.sessID, self.table[3][0]))
        score = c.fetchall()[0][0]
        c.execute('''UPDATE SessionScores SET Score={} wHERE SessionID = {} AND PlayerName = "{}"'''.format(score+1, self.sessID, self.table[3][0]))

        db.commit()

class Placement:

    def __init__(self,master,colour,names, sessID, prev):
        self.master = master
        self.prev = prev
        self.colour = colour
        self.sessID = sessID
        self.names = names
        self.draw_window()

    def close(self):
        self.prev.close()

    def draw_window(self):
        self.master.configure(bg=self.colour)
        self.master.title("Placements")
        self.input_names = [StringVar(),StringVar(),StringVar(),StringVar()]
        Label(self.master, text="Pos",bg=self.colour,width=5).grid(row=0, column=0)
        Label(self.master, text="Name",bg=self.colour,width=28).grid(row=0, column=1)
        Label(self.master, text="",bg=self.colour,width=25).grid(row=1, column=0)
        Label(self.master, text="1st",bg=self.colour,width=5).grid(row=2, column=0)
        Label(self.master, text="2nd",bg=self.colour,width=5).grid(row=4, column=0)
        Label(self.master, text="3rd",bg=self.colour,width=5).grid(row=6, column=0)
        Label(self.master, text="4th",bg=self.colour,width=5).grid(row=8, column=0)
        for i in range(0,4):
            Label(self.master, text="",bg=self.colour,width=25).grid(row=(i*2)+3, column=0)
            Label(self.master, text="",bg=self.colour,width=25).grid(row=(i*2)+3, column=1)
            Entry(self.master, textvariable = self.input_names[i], width=25).grid(row=(i*2)+2, column=1)
        Button(self.master, text="Confirm",bg=self.colour, command=partial(self.scoring)).grid(row=10, column=1)
        Button(self.master, text="Get Pairings",bg=self.colour, command=partial(self.pair)).grid(row=10, column=0)

    def scoring(self):
        accpeted = True
        for i in range(0,4):
            this_accepted_1 = True
            for j in range(0,i):
                if self.input_names[i].get() == self.input_names[j].get():
                    Label(self.master, text="Duplicate Name",bg="#AA0000",width=25).grid(row=(i*2)+3, column=1)
                    accpeted = False
                    this_accepted_1 = False
                elif this_accepted_1 == True:
                    Label(self.master, text="",bg=self.colour,width=25).grid(row=(i*2)+3, column=1)
            if self.input_names[i].get() not in self.names:
                Label(self.master, text="Not a valid input",bg="#AA0000",width=25).grid(row=(i*2)+3, column=1)
                accepted = False
                this_accepted_1 = False
            elif this_accepted_1 == True:
                Label(self.master, text="",bg=self.colour,width=25).grid(row=(i*2)+3, column=1)
        if accpeted == True:
            for i in range(0,4):
                self.input_names[i] = self.input_names[i].get()
            print("Store")
            #Store the top 4 in database HERE
            #Use self.input_names[0], self.input_names[1], self.input_names[2] and self.input_names[3] as the names for 1st, 2nd, 3rd, 4th.
            #Names are inputs so there won't be any problems with brackets here (he says hopefully)
            self.database_input()
            self.master.destroy()
            #I also need to get rid of the previous windows here at this point and idk how to do that

    def database_input(self):
        db = sql.connect("WXGT.db")
        c = db.cursor()
        medal = {0:"Golds",1:"Silvers",2:"Bronzes"}
        for i in range(3):
            c.execute('''SELECT {} FROM SessionScores WHERE SessionID = {} AND PlayerName = "{}"'''.format(medal[i], self.sessID, self.input_names[i]))
            medals = c.fetchall()[0][0]
            print(medals)
            print(i)
            c.execute('''UPDATE SessionScores SET {} = {} WHERE SessionID = {} AND PlayerName = "{}" '''.format(medal[i], medals+1, self.sessID, self.input_names[i]))

            c.execute('''SELECT Score FROM SessionScores WHERE SessionID = {} AND PlayerName = "{}"'''.format(self.sessID, self.input_names[i]))
            score = c.fetchall()[0][0]

            c.execute('''UPDATE SessionScores SET Score={} wHERE SessionID = {} AND PlayerName = "{}"'''.format(score+4-i, self.sessID,self.input_names[i]))

        c.execute('''SELECT Score FROM SessionScores WHERE SessionID = {} AND PlayerName = "{}"'''.format(self.sessID, self.input_names[3]))
        score = c.fetchall()[0][0]
        c.execute('''UPDATE SessionScores SET Score={} wHERE SessionID = {} AND PlayerName = "{}"'''.format(score+1, self.sessID, self.input_names[3]))

        db.commit()

    def pair(self):
        newlevel = Toplevel(self.master)
        win = pairing(newlevel,self.colour,self.names,False)

class twovtwo:

    def __init__(self,master,colour,names, sessID, prev):
        self.master = master
        self.prev = prev
        self.colour = colour
        self.sessID = sessID
        self.names = names
        self.draw_window()

    def close(self):
        self.master.destroy()
        self.prev.close()

    def draw_window(self):
        self.master.configure(bg=self.colour)
        self.master.title("2v2 Placements")
        self.input_names_1 = [StringVar(),StringVar(),StringVar(),StringVar()]
        self.input_names_2 = [StringVar(),StringVar(),StringVar(),StringVar()]
        Label(self.master, text="Pos",bg=self.colour,width=5).grid(row=0, column=0)
        Label(self.master, text="Partner 1",bg=self.colour,width=28).grid(row=0, column=1)
        Label(self.master, text="",bg=self.colour,width=3).grid(row=0, column=2)
        Label(self.master, text="Partner 2",bg=self.colour,width=28).grid(row=0, column=3)
        Label(self.master, text="",bg=self.colour,width=25).grid(row=1, column=0)
        Label(self.master, text="1st",bg=self.colour,width=5).grid(row=2, column=0)
        Label(self.master, text="2nd",bg=self.colour,width=5).grid(row=4, column=0)
        Label(self.master, text="3rd",bg=self.colour,width=5).grid(row=6, column=0)
        Label(self.master, text="4th",bg=self.colour,width=5).grid(row=8, column=0)
        for i in range(0,4):
            Label(self.master, text="+",bg=self.colour,width=3).grid(row=(i*2)+2, column=2)
            Label(self.master, text="",bg=self.colour,width=25).grid(row=(i*2)+3, column=0)
            Label(self.master, text="",bg=self.colour,width=25).grid(row=(i*2)+3, column=1)
            Entry(self.master, textvariable = self.input_names_1[i], width=25).grid(row=(i*2)+2, column=1)
            Entry(self.master, textvariable = self.input_names_2[i], width=25).grid(row=(i*2)+2, column=3)
        Button(self.master, text="Get Pairings",bg=self.colour, command=partial(self.pair)).grid(row=10, column=1)
        Button(self.master, text="Confirm",bg=self.colour, command=partial(self.scoring)).grid(row=10, column=3)

    def scoring(self):
        accpeted = True
        for i in range(0,4):
            this_accepted_1 = True
            this_accepted_2 = True
            for j in range(0,i):
                if self.input_names_1[i].get() == self.input_names_1[j].get() or self.input_names_1[i].get() == self.input_names_2[j].get():
                    Label(self.master, text="Duplicate Name",bg="#AA0000",width=25).grid(row=(i*2)+3, column=1)
                    accpeted = False
                    this_accepted_1 = False
                elif this_accepted_1 == True:
                    Label(self.master, text="",bg=self.colour,width=25).grid(row=(i*2)+3, column=1)
                if self.input_names_2[i].get() == self.input_names_1[j].get() or self.input_names_2[i].get() == self.input_names_2[j].get():
                    Label(self.master, text="Duplicate Name",bg="#AA0000",width=25).grid(row=(i*2)+3, column=3)
                    accpeted = False
                    this_accepted_2 = False
                elif this_accepted_2 == True:
                    Label(self.master, text="",bg=self.colour,width=25).grid(row=(i*2)+3, column=3)
            if self.input_names_1[i].get() == self.input_names_2[i].get():
                Label(self.master, text="Duplicate Name",bg="#AA0000",width=25).grid(row=(i*2)+3, column=3)
                accpeted = False
                this_accepted_2 = False
            elif this_accepted_2 == True:
                Label(self.master, text="",bg=self.colour,width=25).grid(row=(i*2)+3, column=3)
            if self.input_names_1[i].get() not in self.names:
                Label(self.master, text="Not a valid input",bg="#AA0000",width=25).grid(row=(i*2)+3, column=1)
                accepted = False
                this_accepted_1 = False
            elif this_accepted_1 == True:
                Label(self.master, text="",bg=self.colour,width=25).grid(row=(i*2)+3, column=1)
            if self.input_names_2[i].get() not in self.names:
                Label(self.master, text="Not a valid input",bg="#AA0000",width=25).grid(row=(i*2)+3, column=3)
                accepted = False
                this_accepted_2 = False
            elif this_accepted_2 == True:
                Label(self.master, text="",bg=self.colour,width=25).grid(row=(i*2)+3, column=3)
        if accpeted == True:
            for i in range(0,4):
                self.input_names_1[i] = self.input_names_1[i].get()
                self.input_names_2[i] = self.input_names_2[i].get()
            print("Store")
            #Store the top 4 in database HERE
            #Use self.input_names_1[0], self.input_names_1[1], self.input_names_1[2] and self.input_names_1[3] as names for 1st, 2nd, 3rd, 4th.
            #Also use self.input_names_2[0], self.input_names_2[1], self.input_names_2[2] and self.input_names_2[3] as the other names for 1st, 2nd, 3rd, 4th.
            #As before, names are inputs so there won't be any problems with brackets here (again, hopefully)
            self.database_input()
            self.master.destroy()
            #Same issue again, I need to get rid of the previous windows at this point and idk how to do that

    def database_input(self):
        db = sql.connect("WXGT.db")
        c = db.cursor()
        medal = {0:"Golds",1:"Silvers",2:"Bronzes"}
        for j in range(1,3):
            for i in range(3):
                c.execute('''SELECT {} FROM SessionScores WHERE SessionID = {} AND PlayerName = "{}"'''.format(medal[i], self.sessID, eval("self.input_names_"+str(j)+"[i]")))
                medals = c.fetchall()[0][0]
                print(medals)
                c.execute('''UPDATE SessionScores SET {} = {} WHERE SessionID = {} AND PlayerName = "{}" '''.format(medal[i], medals+1, self.sessID, eval("self.input_names_"+str(j)+"[i]")))

                c.execute('''SELECT Score FROM SessionScores WHERE SessionID = {} AND PlayerName = "{}"'''.format(self.sessID,eval("self.input_names_"+str(j)+"[i]")))
                score = c.fetchall()[0][0]

                c.execute('''UPDATE SessionScores SET Score={} wHERE SessionID = {} AND PlayerName = "{}"'''.format(score+4-i, self.sessID,eval("self.input_names_"+str(j)+"[i]")))

            c.execute('''SELECT Score FROM SessionScores WHERE SessionID = {} AND PlayerName = "{}"'''.format(self.sessID, eval("self.input_names_"+str(j)+"[3]")))
            score = c.fetchall()[0][0]
            c.execute('''UPDATE SessionScores SET Score={} wHERE SessionID = {} AND PlayerName = "{}"'''.format(score+1, self.sessID, eval("self.input_names_"+str(j)+"[3]")))

        db.commit()

    def pair(self):
        newlevel = Toplevel(self.master)
        win = pairing(newlevel,self.colour,self.names,True)

class pairing:

    def __init__(self,master,colour,names,twovtwo):
        self.master = master
        self.colour = colour
        self.names = names
        self.twovtwo = twovtwo
        self.draw_window()

    def draw_window(self):
        self.master.configure(bg=self.colour)
        x = []
        for i in range(0,len(self.names)):
            x.append(self.names[i])
        people = []
        for i in range(0,len(x)):
            people.append(random.choice(x))
            x.remove(people[i])
        Label(self.master, text="",bg=self.colour,width=25).grid(row=0, column=0)
        Label(self.master, text="",bg=self.colour,width=5).grid(row=0, column=1)
        Label(self.master, text="",bg=self.colour,width=25).grid(row=0, column=2)
        Label(self.master, text="",bg=self.colour,width=5).grid(row=0, column=3)
        Label(self.master, text="",bg=self.colour,width=25).grid(row=0, column=4)
        Label(self.master, text="",bg=self.colour,width=25).grid(row=7, column=0)
        for i in range(0,int(len(self.names)//4)):
            Label(self.master, text=people[(i*4)],bg=self.colour,width=25).grid(row=(i*7)+1, column=0)
            if self.twovtwo == True:
                Label(self.master, text="+",bg=self.colour,width=5).grid(row=(i*7)+1, column=1)
            else:
                Label(self.master, text="Vs",bg=self.colour,width=5).grid(row=(i*7)+1, column=1)
            Label(self.master, text=people[(i*4)+1],bg=self.colour,width=25).grid(row=(i*7)+1, column=2)
            Label(self.master, text="",bg=self.colour,width=25).grid(row=(i*7)+2, column=0)
            Label(self.master, text="Vs",bg=self.colour,width=5).grid(row=(i*7)+3, column=2)
            Label(self.master, text="",bg=self.colour,width=25).grid(row=(i*7)+4, column=0)
        for i in range(0,int(len(self.names)//4)):
            Label(self.master, text=people[(i*4)+2],bg=self.colour,width=25).grid(row=(i*7)+5, column=2)
            if self.twovtwo == True:
                Label(self.master, text="+",bg=self.colour,width=5).grid(row=(i*7)+5, column=3)
            else:
                Label(self.master, text="Vs",bg=self.colour,width=5).grid(row=(i*7)+5, column=3)
            Label(self.master, text=people[(i*4)+3],bg=self.colour,width=25).grid(row=(i*7)+5, column=4)
            Label(self.master, text="",bg=self.colour,width=25).grid(row=(i*7)+6, column=0)
        

def create_window(root, colour, names,event_type,to_final, sessID, prev):
    if event_type == "Numbers":
        window = Numbers(root,colour,names,to_final, sessID, prev)
        root.mainloop()
    elif event_type == "2v2":
        window = twovtwo(root,colour,names, sessID, prev)
        root.mainloop()
    else:
        window = Placement(root,colour,names, sessID, prev)
        root.mainloop()

