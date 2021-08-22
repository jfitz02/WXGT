#Tom Stuart
#05.06.20
#WXGT

import tkinter
import Display_Player_Stats
import Overall_Leaderboard
import Display_Previous_Season
import Overall_Stats
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

class Select_Stat:

    def __init__(self,master,colour):
        self.master = master
        self.colour = colour
        self.bg_colours = {"Red":"#AA0000", "Gold":"#FFFFFF", "Green":"#2CB322", "Purple":"#8F06A1", "Yellow":"#E4ED42", "Blue":"#12C5E0"}
        self.draw_window()

    def draw_window(self):
        self.master.configure(bg=self.bg_colours[self.colour])
        self.master.title("Pick Stats")
        Options = ["Player Individual Stats","Overall Leaderboard","Show Previous Session Leaderboard","Overall Interesting Stats"]
        self.Selected_Option = StringVar(self.master)
        self.Selected_Option.set("Player Individual Stats")
        Label(self.master, text=" ",bg=self.bg_colours[self.colour],width=5).grid(row=0, column=0)
        Label(self.master, text=" ",bg=self.bg_colours[self.colour],width=5).grid(row=0, column=2)
        Label(self.master, text=" ",bg=self.bg_colours[self.colour],width=5).grid(row=3, column=1)
        self.initial_label = Label(self.master, text="Stat Type",bg=self.bg_colours[self.colour])
        self.initial_label.grid(row=1, column=1)
        self.initial_option = OptionMenu(self.master,self.Selected_Option, *Options)
        self.initial_option.grid(row=2,column=1)
        self.initial_button = Button(self.master, text="Confirm",bg=self.bg_colours[self.colour], command=partial(self.open_next_window,self.Selected_Option))
        self.initial_button.grid(row=4, column=1)

    def open_next_window(self,option):
        if option.get() == "Player Individual Stats":
            newlevel = Toplevel(self.master)
            win = Display_Player_Stats.create_window(newlevel,self.colour)
        if option.get() == "Overall Leaderboard":
            newlevel = Toplevel(self.master)
            win = Overall_Leaderboard.create_window(newlevel,self.colour)
        if option.get() == "Show Previous Session Leaderboard":
            newlevel = Toplevel(self.master)
            win = Display_Previous_Season.create_window(newlevel,self.colour)
        if option.get() == "Overall Interesting Stats":
            newlevel = Toplevel(self.master)
            win = Overall_Stats.create_window(newlevel,self.colour)

def create_window(root, colour):
    window = Select_Stat(root,colour)
    root.mainloop()





        
