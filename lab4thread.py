"""
Benjamin Chen
Weather Application with Multithreading
"""
from logging import info
import requests
import tkinter as tk
import tkinter.messagebox as tkmb
from tkinter import filedialog as fd
import os
from threading import *

class DialogueWin(tk.Toplevel):
    def __init__(self, master, *args, **kwargs):
        """
        constructor for Dialogue Window
        input: *args and **kwargs which is the information that is displayed in Dialogue Win
        constructs Dialogue GUI Window
        """
        super().__init__()
        self.focus_set()
        self.grab_set()
        self.transient()

        information = []
        for x in args:
            information.append(x)
        for x in kwargs:
            information.append(x)
        counter = 0
        self.controlVar = tk.IntVar(master) #user input

        self.controlVar.set(0)
        for x in information[0]:
            tk.Radiobutton(self, text = str(x), variable = self.controlVar, value = counter).grid(column = 0, sticky = 'w')
            counter +=1
        tk.Button(self, text = "Ok", command = self.destroy).grid()
        self.protocol('WM_DELETE_WINDOW', self.close_app)

    def close_app(self):
        self.controlVar.set(-1)
        self.destroy()
    def getChoice(self):
        return self.controlVar.get()
class MainWin(tk.Tk):
    def __init__(self):
        """
        constructor for MainWin tkinter object
        input: list of cities and its respective information
        constructs GUI window
        """
        self.madechoice = False
        self.inBox = []
        super().__init__()
        self.title('Welcome to the weather app')
        self.box = tk.Listbox(self, height = 12, width = 60, selectmode = "multiple")
        tk.Button(self, text = "Choose a City", command = self.city).pack()

        S = tk.Scrollbar(self, orient="vertical")
        S.config(command = self.box.yview)
        S.pack(side = 'right', fill = 'y')
        self.box.config(yscrollcommand = S.set)
        self.box.pack(side = "left", fill = 'both', expand = True)

        
        self.information = []
        
        thread = Thread(target = self.getInfo) #creates 12 child threads
        thread.setDeamon(true)
        thread.start()
        thread.join()
        """
        self.getInfo()
        """
        self.box.pack(side = "left", fill = 'both', expand = True)
        self.protocol('WM_DELETE_WINDOW', self.close_app)

    def getInfo(self):
        listOfCities = ['Berkeley', 'Cupertino', 'Davis', 'Irvine', 'Los Angeles', 'Palo Alto', 
        'Sacramento', 'San Diego', 'San Jose', 'Santa Barbara', 'Santa Cruz']
        for x in listOfCities:
            page = requests.get('http://api.openweathermap.org/data/2.5/weather?q=%s,CA,US&appid=ca0489f2090d79b9ca7f4ca1514ffd90'%(x))
            resultDict = page.json()
            self.information.append("%s: %i degrees, %s"%(x,round(resultDict['main']['temp'] - 273.15),resultDict['weather'][0]['description']))


    def city(self):
        listOfCities = ['Berkeley (UCB)', 'Cupertino (De Anza)', 'Davis (UCD)', 'Irvine(UCI)', 'Los Angeles (UCLA)', 'Palo Alto (Stanford)', 
        'Sacramento (Sac State)', 'San Diego (UCSD)', 'San Jose (SJSU)', 'Santa Barbara (UCSB)', 'Santa Cruz (UCSC)']
        d = DialogueWin(self, listOfCities)
        self.wait_window(d)
        if not d.getChoice() == -1:
            self.box.insert('end', self.information[d.getChoice()])
            self.inBox.append(self.information[d.getChoice()])
            self.madechoice = True #sets madechoice to true so application knows to prompt user to save the choice in text file

    def close_app(self):
        if self.madechoice:
            saving = tkmb.askokcancel(title = 'Save', message = 'Save your search in a directory of your choice?')
            if saving:
                filename = fd.askdirectory(title = 'Open a file', initialdir = os.path.dirname(os.path.realpath(__file__)))
                f = open(filename + '/userChoice.txt', 'w')
                for ele in self.inBox:
                    f.write(ele + '\n')
        self.destroy()

app = MainWin()
app.mainloop()
