"""
Benjamin Chen
Weather Application with Multiprocessing
"""
from logging import info
import requests
import tkinter as tk
import tkinter.messagebox as tkmb
from tkinter import filedialog as fd
import os
import multiprocessing

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
        for x in args: #populates information with arguments from method call in MainWin
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
        self.protocol('WM_DELETE_WINDOW', self.close_app) #calls the close_app method when the window closes


    def close_app(self):
        self.controlVar.set(-1) #sets controlVar to one so there will not be any change to MainWin
        self.destroy()

    def getChoice(self):
        return self.controlVar.get()


class MainWin(tk.Tk):
    def __init__(self, information):
        """
        constructor for MainWin tkinter object
        input: list of cities and its respective information
        constructs GUI window
        """
        self.information = information
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

        self.box.pack(side = "left", fill = 'both', expand = True)
        self.protocol('WM_DELETE_WINDOW', self.close_app)
    
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
                filename = fd.askdirectory(title = 'Open a file', initialdir = os.path.dirname(os.path.realpath(__file__))) #initialdir is the directory the file is in currently
                f = open(filename + '/userChoice.txt', 'w')
                for ele in self.inBox:
                    f.write(ele + '\n')
        self.destroy()

def getInfo(cityName):
    """
    api call method for a certain city
    input: name of city
    output: string with the city's weather information
    """
    page = requests.get('http://api.openweathermap.org/data/2.5/weather?q=%s,CA,US&appid=ca0489f2090d79b9ca7f4ca1514ffd90'%(cityName))
    resultDict = page.json()
    information = "%s: %i degrees, %s"%(cityName,round(resultDict['main']['temp'] - 273.15),resultDict['weather'][0]['description'])
    return information

#multiprocess pool map block
if __name__ == '__main__':
    pool = multiprocessing.Pool(processes = 4)
    information = pool.map(getInfo,['Berkeley', 'Cupertino', 'Davis', 'Irvine', 'Los Angeles', 'Palo Alto', 
    'Sacramento', 'San Diego', 'San Jose', 'Santa Barbara', 'Santa Cruz']) #list of cities that weather info is needed
    app = MainWin(information)
    app.mainloop()

"""
Order from slowest to fastest:
in series, multiprocessing, multithreading

In series is obviously the slowest out of the three because it does not utilize parallelism. The API calls for in series involes having to
call the API one time, wait for the process to finish, then call the API another time for a total of 12 times. The task is executed one after
the other as opposed to multiprocessing and multithreading. 

In multiprocesses and multithreading, the API calls are executed simultaneously (in the case of multithreading,
the threads run tasks almost at the same time due to the GIL).

Between multiprocessing and multithreading, in this project in particular, because we are only dealing with 12 API calls,
multithreading is faster. Because of the 12 API calls and therefore a smaller data size, multithreading is faster because
of multiprocessing's bigger use of memory in the OS. Furthermore, due to the use of multiprocessing pools, it takes more method calls
and therefore more time to set up.
"""