import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from sshy_app.tasks import *

class Gui(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.N+tk.E+tk.W+tk.S)
        self.createWidgets()

    def createWidgets(self):
        top=self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        #self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)   
        self.rowconfigure(8, weight=1)

        self.hostLabel = tk.Label(self, text="Host")
        self.hostLabel.grid(padx=5, sticky=tk.W+tk.N)
        self.hostEntry = tk.Entry(self)
        self.hostEntry.grid(padx=5, sticky=tk.N+tk.E+tk.W)

        self.userLabel = tk.Label(self, text="User")
        self.userLabel.grid(padx=5, pady=(10,0), sticky=tk.W+tk.N)
        self.userEntry = tk.Entry(self)
        self.userEntry.grid(padx=5, sticky=tk.E+tk.W+tk.N)
        
        self.passwordLabel = tk.Label(self, text="Password")
        self.passwordLabel.grid(padx=5, pady=(10,0), sticky=tk.NW)
        self.passwordEntry = tk.Entry(self, show="*")
        self.passwordEntry.grid(padx=5, sticky=tk.N+tk.E+tk.W)
        

    
        self.doItButton = tk.Button(self, text='Do it!',
            command=self.doit)
        self.doItButton.grid(padx=5, pady=(10,0))
        
        self.logLabel = tk.Label(self, text="Log").grid(padx=5, pady=(10,0), sticky=tk.N+tk.W)
        self.logEntry = ScrolledText(self, bg="#EEE")
        self.logEntry.configure(state='disabled')
        self.logEntry.grid(padx=5, sticky=tk.N+tk.E+tk.W+tk.S, pady=(0,5))

    def doit(self):
        TaskBase.TaskBase(self, host=self.hostEntry.get(), username=self.userEntry.get(), password=self.passwordEntry.get()).runDefaults()

    def log(self, message):
        self.logEntry.configure(state='normal')
        self.logEntry.insert(tk.INSERT, message+"\n")
        self.logEntry.see(tk.END)
        self.logEntry.configure(state='disabled')

class GuiRunner:
    def run(self):
        app = Gui()
        app.master.title('SSHy')
        app.mainloop()                  