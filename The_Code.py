#Tom Stuart
#26.05.20
#WXGT
import tkinter
import Add_Event
import Select_Stat
import Choose_Event
import Leaderboard
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

class Start_Screen:

    def __init__(self,master):
        self.master = master
        self.draw_window()

    def draw_window(self):
        self.master.configure(bg="#AA0000")
        self.master.title("WXGT")
        Button(self.master, text="View WXGT Records", bg="#AA0000",command=self.records,width=20,height=15).grid(row=0,column=0)
        Button(self.master, text="Start New WXGT", bg="#AA0000",command=self.start_session,width=20,height=15).grid(row=0,column=2)
        self.img = PhotoImage(file="WXGT Red.PNG")
        canvas = Canvas(self.master,bg="#AA0000",width=self.img.width(),height=self.img.height(),highlightthickness = 0, bd = 0)
        canvas.grid(row = 0,column = 1)
        canvas.create_image(0,0,anchor=NW,image=self.img)

    def records(self):
        newlevel = Toplevel(self.master)
        win = Select_Season(newlevel, False)

    def start_session(self):
        newlevel = Toplevel(self.master)
        win = Select_Season(newlevel, True)

class Select_Season:

    def __init__(self,master,starting):
        self.master = master
        self.starting = starting
        self.draw_window()

    def draw_window(self):
        self.master.title("Select Edition")
        self.green = PhotoImage(file="Edition Green.PNG")
        self.purple = PhotoImage(file="Edition Purple.PNG")
        self.yellow = PhotoImage(file="Edition Yellow.PNG")
        self.gold = PhotoImage(file="Edition Gold.PNG")
        self.blue = PhotoImage(file="Edition Blue.PNG")
        green_button = Button(self.master,bg="#2CB322",image=self.green,command=self.green_load,width=250,height=50).grid(row=1,column=0)
        purple_button = Button(self.master,bg="#8F06A1",image=self.purple,command=self.purple_load,width=250,height=50).grid(row=2,column=0)
        yellow_button = Button(self.master,bg="#E4ED42",image=self.yellow,command=self.yellow_load,width=250,height=50).grid(row=3,column=0)
        gold_button = Button(self.master,bg="#FFFFFF",image=self.gold,command=self.gold_load,width=250,height=50).grid(row=4,column=0)
        blue_button = Button(self.master,bg="#12C5E0",image=self.blue,command=self.blue_load,width=250,height=50).grid(row=0,column=0)
        
        
    def green_load(self):
        if self.starting == True:
            newlevel = Toplevel(self.master)
            win = Select_Players(newlevel, "Green")
        else:
            newlevel = Toplevel(self.master)
            win = Select_Stat.create_window(newlevel,"Green")

    def purple_load(self):
        if self.starting == True:
            newlevel = Toplevel(self.master)
            win = Select_Players(newlevel, "Purple")
        else:
            newlevel = Toplevel(self.master)
            win = Select_Stat.create_window(newlevel,"Purple")
            
    def yellow_load(self):
        if self.starting == True:
            newlevel = Toplevel(self.master)
            win = Select_Players(newlevel, "Yellow")
        else:
            newlevel = Toplevel(self.master)
            win = Select_Stat.create_window(newlevel,"Yellow")
            
    def gold_load(self):
        if self.starting == True:
            newlevel = Toplevel(self.master)
            win = Select_Players(newlevel, "Gold")
        else:
            newlevel = Toplevel(self.master)
            win = Select_Stat.create_window(newlevel,"Gold")
            
    def blue_load(self):
        if self.starting == True:
            newlevel = Toplevel(self.master)
            win = Select_Players(newlevel, "Blue")
        else:
            newlevel = Toplevel(self.master)
            win = Select_Stat.create_window(newlevel,"Blue")


class Select_Players:

    def __init__(self,master,colour):
        self.master = master
        self.colour = colour
        self.bg_colours = {"Red":"#AA0000", "Gold":"#FFFFFF", "Green":"#2CB322", "Purple":"#8F06A1", "Yellow":"#E4ED42", "Blue":"#12C5E0"}
        self.draw_window()

    def draw_window(self):
        self.master.configure(bg=self.bg_colours[self.colour])
        self.master.title("Enter Competitors")
        Label(self.master, text=" ",bg=self.bg_colours[self.colour],width=5).grid(row=0, column=0)
        Label(self.master, text=" ",bg=self.bg_colours[self.colour],width=5).grid(row=0, column=2)
        Label(self.master, text="Competitors:",bg=self.bg_colours[self.colour]).grid(row=0, column=1)
        self.Names=[StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar()]
        for i in range(1,9):
            Label(self.master, text=" ",bg=self.bg_colours[self.colour],width=5).grid(row=(i*2)+1, column=1)
            Entry(self.master, textvariable = self.Names[i-1], width=25).grid(row=(i*2)+2, column=1)
        Label(self.master, text=" ",bg=self.bg_colours[self.colour],width=5).grid(row=19, column=1)
        Button(self.master, text="Confirm",bg=self.bg_colours[self.colour], command=self.destroy_window).grid(row=20, column=1)

    def destroy_window(self):
        self.new_names = [False,False,False,False,False,False,False,False]
        amount = 0
        for i in range(0,8):
            new_player = self.check_players(self.Names[i].get())
            if new_player:
                self.new_names[i] = True
                amount += 1
        if amount>0:
            self.creating = Label(self.master, text=("Creating "+str(amount)+" new player accounts. Is this correct?"),bg=self.bg_colours["Red"],width=36)
            self.creating.grid(row=19, column=1)
            self.no_button = Button(self.master, text="No, go back",bg=self.bg_colours[self.colour], command=self.back_it_up)
            self.no_button.grid(row=20, column=1)
            self.yes_button = Button(self.master, text="Yes, proceed",bg=self.bg_colours[self.colour], command=self.add_peeps)
            self.yes_button.grid(row=21, column=1)
        else:
            newlevel = Toplevel(self.master)
            for i in range(0,8):
                self.Names[i] = self.Names[i].get()
            win = Creation(newlevel, self.colour, self.Names, self)

    def back_it_up(self):
        self.creating.destroy()
        self.no_button.destroy()
        self.yes_button.destroy()
        
    def check_players(self, name):
        db = sql.connect("WXGT.db")
        c = db.cursor()

        c.execute('''SELECT PlayerName FROM Players WHERE PlayerName == "{}"'''.format(name))

        data = c.fetchall()

        db.commit()

        if len(data) == 0:
            return True
        return False

    

    def add_peeps(self):
        for i in range(0,8):
            self.Names[i] = self.Names[i].get()
        db = sql.connect("WXGT.db")
        c = db.cursor()
        for i, name in enumerate(self.Names):
            if self.new_names[i] == True:
                c.execute('''INSERT INTO Players(PlayerName) VALUES("{}")'''.format(name))

        db.commit()
        newlevel = Toplevel(self.master)
        win = Creation(newlevel, self.colour, self.Names, self)


class Creation:

    def __init__(self, master, colour, names, prev):
        self.edition = {"Gold":"CHAMPIONS", "Green":"SF", "Purple":"UNI", "Yellow":"POSTUNI", "Blue":"QF"}
        self.prev = prev
        self.colour = colour
        self.names = names
        self.create_session()
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.close)
        self.bg_colours = {"Red":"#AA0000", "Gold":"#FFFFFF", "Green":"#2CB322", "Purple":"#8F06A1", "Yellow":"#E4ED42", "Blue":"#12C5E0"}
       
        self.draw_window()

    def close(self):
        self.prev.master.destroy()

    def get_season_number(self):
        db = sql.connect("WXGT.db")
        c = db.cursor()

        c.execute('''SELECT SessionID FROM Session WHERE SessionType = "{}"'''.format(self.edition[self.colour]))
        data = c.fetchall()

        db.commit()

        return len(data)
    def draw_window(self):
        self.master.configure(bg=self.bg_colours[self.colour])
        self.WXGT = PhotoImage(file="WXGT "+self.colour+".PNG")
        self.Edition = PhotoImage(file="Edition "+self.colour+".PNG")
        Button(self.master, text="Start an event", bg=self.bg_colours[self.colour],command=self.start_event,width=20,height=5).grid(row=0,column=0)
        Button(self.master, text="Add new event", bg=self.bg_colours[self.colour],command=self.add_event,width=20,height=5).grid(row=0,column=2)
        Label(self.master,bg=self.bg_colours[self.colour],image=self.WXGT).grid(row=1,column=1)
        if self.colour != "Blue":
            self.Season = PhotoImage(file="Season "+self.colour+".PNG")
            number = self.get_season_number()
            self.C = PhotoImage(file="C "+self.colour+".PNG")
            self.L = PhotoImage(file="L "+self.colour+".PNG")
            self.X = PhotoImage(file="X "+self.colour+".PNG")
            self.V = PhotoImage(file="V "+self.colour+".PNG")
            self.I = PhotoImage(file="I "+self.colour+".PNG")
            numeral = []
            total_width = self.Season.width()+10
            while number>=100:
                numeral.append("C")
                number = number - 100
                total_width += self.C.width()-2
            while number>=90:
                numeral.append("X")
                numeral.append("C")
                number = number - 100
                total_width += self.C.width()-2
                total_width += self.X.width()-2
            while number>=50:
                numeral.append("L")
                number = number - 50
                total_width += self.L.width()-2
            while number>=40:
                numeral.append("X")
                numeral.append("L")
                number = number - 40
                total_width += self.L.width()-2
                total_width += self.X.width()-2
            while number>=10:
                numeral.append("X")
                number = number - 10
                total_width += self.X.width()-2
            while number>=9:
                numeral.append("I")
                numeral.append("X")
                number = number - 9
                total_width += self.I.width()-2
                total_width += self.X.width()-2
            while number>=5:
                numeral.append("V")
                number = number - 5
                total_width += self.V.width()-2
            while number>=4:
                numeral.append("I")
                numeral.append("V")
                number = number - 4
                total_width += self.I.width()-2
                total_width += self.V.width()-2
            while number>=1:
                numeral.append("I")
                number = number - 1
                total_width += self.I.width()-2
            canvas = Canvas(self.master,bg=self.bg_colours[self.colour],width=total_width,height=self.Season.height(),highlightthickness = 0, bd = 0)
            canvas.grid(row = 2,column = 1)
            canvas.create_image(0,0,anchor=NW,image=self.Season)
            x_value = self.Season.width()+8
            for i in range(0,len(numeral)):
                if numeral[i] == "C":
                    canvas.create_image(x_value,0,anchor=NW,image=self.C)
                    x_value += self.C.width()-2
                elif numeral[i] == "L":
                    canvas.create_image(x_value,0,anchor=NW,image=self.L)
                    x_value += self.L.width()-2
                elif numeral[i] == "X":
                    canvas.create_image(x_value,0,anchor=NW,image=self.X)
                    x_value += self.X.width()-2
                elif numeral[i] == "V":
                    canvas.create_image(x_value,0,anchor=NW,image=self.V)
                    x_value += self.V.width()-2
                elif numeral[i] == "I":
                    canvas.create_image(x_value,0,anchor=NW,image=self.I)
                    x_value += self.I.width()-2
            Label(self.master,bg=self.bg_colours[self.colour],image=self.Edition).grid(row=3,column=1)
            Button(self.master, text="View current leaderboard", bg=self.bg_colours[self.colour],command=self.show_leaderboard,width=20,height=5).grid(row=4,column=0)
            Button(self.master, text="Finish Session", bg=self.bg_colours[self.colour],command=self.finish,width=20,height=5).grid(row=4,column=2)
        else:
            Label(self.master,bg=self.bg_colours[self.colour],image=self.Edition).grid(row=2,column=1)
            Button(self.master, text="View current leaderboard", bg=self.bg_colours[self.colour],command=self.show_leaderboard,width=20,height=5).grid(row=3,column=0)
            Button(self.master, text="Finish Session", bg=self.bg_colours[self.colour],command=self.finish,width=20,height=5).grid(row=3,column=2)

    def start_event(self):
        newlevel = Toplevel(self.master)
        win = Choose_Event.create_window(newlevel,self.bg_colours[self.colour],self.names, self.next_id, self)

    def add_event(self):
        newlevel = Toplevel(self.master)
        win = Add_Event.create_window(newlevel,self.bg_colours[self.colour], self)

    def create_session(self):
        self.next_id = idf.get_next_id("WXGT.db","Session", "SessionID")
        db = sql.connect("WXGT.db")
        c = db.cursor()

        c.execute('''INSERT INTO Session(SessionID, SessionType) VALUES({}, "{}")'''.format(self.next_id, self.edition[self.colour]))

        for name in self.names:
            c.execute('''INSERT INTO SessionScores(PlayerName, SessionID, Score, Golds, Silvers, Bronzes) VALUES("{}", {}, {}, {}, {}, {})'''.format(name, self.next_id, 0, 0, 0, 0))


        db.commit()

    def show_leaderboard(self):
        newLevel = Toplevel(self.master)
        win = Leaderboard.create_window(newLevel, self.next_id, self.colour, False, self)

    def finish(self):
        newLevel = Toplevel(self.master)
        win = Leaderboard.create_window(newLevel, self.next_id, self.colour,True, self)
        
root = Tk()
window = Start_Screen(root)
root.mainloop()
