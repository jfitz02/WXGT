#Tom Stuart
#01.06.20
#WXGT
import tkinter
from tkinter import *
from functools import partial
import sqlite3 as sql
import ID_fetcher as idf

#red = #AA0000
#gold = #FFFFFF
#green = #2CB322
#purple = #8F06A1
#yellow = #E4ED42
#blue = #12C5E0

class Add_Event:

    def __init__(self,master,colour, prev):
        self.master = master
        self.prev = prev
        self.draw_window(colour)

    def close(self):
        self.prev.destroy()

    def draw_window(self,colour):
        self.master.configure(bg=colour)
        self.master.title("Add event")
        Event_Types = ["Placement Only","Numbers to Placement","Numbers Only", "2v2"]
        self.Selected_Type = StringVar(self.master)
        self.Selected_Type.set("Placement Only")
        Console = ["Wii","Xbox"]
        self.Selected_Console = StringVar(self.master)
        self.Selected_Console.set("Wii")
        Label(self.master, text=" ",bg=colour,width=5).grid(row=0, column=0)
        Label(self.master, text=" ",bg=colour,width=5).grid(row=0, column=2)
        Label(self.master, text=" ",bg=colour,width=5).grid(row=3, column=1)
        Label(self.master, text=" ",bg=colour,width=5).grid(row=6, column=1)
        Label(self.master, text=" ",bg=colour,width=5).grid(row=9, column=1)
        Label(self.master, text="Name of event",bg=colour).grid(row=1, column=1)
        self.Name = StringVar()
        Entry(self.master, textvariable = self.Name, width=25).grid(row=2, column=1)
        Label(self.master, text="Console",bg=colour).grid(row=4, column=1)
        OptionMenu(self.master,self.Selected_Console, *Console).grid(row=5,column=1)
        Label(self.master, text="Event Types",bg=colour).grid(row=7, column=1)
        OptionMenu(self.master,self.Selected_Type, *Event_Types).grid(row=8,column=1)
        Button(self.master, text="Confirm",bg=colour, command=self.input_to_database).grid(row=10, column=1)

    def input_to_database(self):
        db = sql.connect("WXGT.db")
        c = db.cursor()

        next_id = idf.get_next_id("WXGT.db", "Games", "GameID")

        c.execute('''INSERT INTO  Games(GameID, Name, Type, Console) VALUES({},"{}","{}","{}")'''.format(next_id,  self.Name.get(), self.Selected_Type.get(), self.Selected_Console.get()))

        db.commit()
        self.master.destroy()
    
def create_window(root, colour, prev):
    window = Add_Event(root,colour, prev)
    root.mainloop()
