#Tom Stuart
#01.06.20
#WXGT
import Run_Event
import tkinter
from tkinter import *
from functools import partial
import sqlite3 as sql

#red = #AA0000
#gold = #FFFFFF
#green = #2CB322
#purple = #8F06A1
#yellow = #E4ED42
#blue = #12C5E0

class Choose_Event:

    def __init__(self,master,colour,names, sessID, prev):
        self.master = master
        self.prev = prev
        self.names = names
        self.colour = colour
        self.sessID = sessID
        self.draw_window(colour)

    def draw_window(self,colour):
        self.master.configure(bg=colour)
        self.master.title("Choose event")
        Console = ["Wii","Xbox"]
        self.Selected_Console = StringVar(self.master)
        self.Selected_Console.set("Wii")
        Label(self.master, text=" ",bg=colour,width=5).grid(row=0, column=0)
        Label(self.master, text=" ",bg=colour,width=5).grid(row=0, column=2)
        Label(self.master, text=" ",bg=colour,width=5).grid(row=3, column=1)
        self.initial_label = Label(self.master, text="Console",bg=colour)
        self.initial_label.grid(row=1, column=1)
        self.initial_option = OptionMenu(self.master,self.Selected_Console, *Console)
        self.initial_option.grid(row=2,column=1)
        self.initial_button = Button(self.master, text="Confirm",bg=colour, command=partial(self.continue_draw,colour,self.Selected_Console))
        self.initial_button.grid(row=4, column=1)

    def close(self):
        self.prev.close()

    def continue_draw(self,colour,Console):
        Console = Console.get()
        self.initial_label.destroy()
        self.initial_option.destroy()
        self.initial_button.destroy()
        Xbox_Events, Wii_Events = self.get_data()
        Label(self.master, text="Event",bg=colour).grid(row=1, column=1)
        print(self.Selected_Console.get())
        print(self.Selected_Console)
        if Console == "Wii":
            self.Selected_Event = StringVar(self.master)
            self.Selected_Event.set(Wii_Events[0])
            OptionMenu(self.master,self.Selected_Event, *Wii_Events).grid(row=2,column=1)
        else:
            self.Selected_Event = StringVar(self.master)
            self.Selected_Event.set(Xbox_Events[0])
            OptionMenu(self.master,self.Selected_Event, *Xbox_Events).grid(row=2,column=1)
        Button(self.master, text="Confirm",bg=colour, command=partial(self.destroy_window,self.Selected_Event)).grid(row=4, column=1)

    def get_data(self):
        db = sql.connect("WXGT.db")
        c = db.cursor()

        c.execute('''SELECT Name FROM Games WHERE Console == "Xbox"''')
        data = c.fetchall()
        print(data, "data")

        if len(data) == 0:
            xbox = []
        else:
            xbox = []
            for game in data:
                xbox.append(game[0])

        c.execute('''SELECT Name FROM Games WHERE Console == "Wii"''')
        data = c.fetchall()
        print(data, "data")
        if len(data) == 0:
            wii = []
        else:
            wii = []
            for game in data:
                wii.append(game[0])
        return xbox, wii
    def destroy_window(self,Event):
        db = sql.connect("WXGT.db")
        c = db.cursor()

        c.execute('''SELECT Type FROM Games WHERE Name == "{}"'''.format(Event.get()))
        Type = c.fetchall()
        print(Type[0][0])
        if Type[0][0] == "Placement Only":
            newlevel = Toplevel(self.master)
            win = Run_Event.create_window(newlevel,self.colour,self.names,"Placement",False, self.sessID, self.master)
        elif Type[0][0] == "2v2":
            newlevel = Toplevel(self.master)
            win = Run_Event.create_window(newlevel,self.colour,self.names,"2v2",False, self.sessID, self.master)
        elif Type[0][0] == "Numbers Only":
            newlevel = Toplevel(self.master)
            win = Run_Event.create_window(newlevel,self.colour,self.names,"Numbers",False, self.sessID, self.master)
        else:
            newlevel = Toplevel(self.master)
            win = Run_Event.create_window(newlevel,self.colour,self.names,"Numbers",True, self.sessID, self.master)
    
        self.master.destroy()
def create_window(root, colour, names, sessID, prev):
    window = Choose_Event(root,colour,names, sessID, prev)
    root.mainloop()

            
