from tkinter import messagebox
from tkinter import *
from tkinter import ttk
from tkinter import Label
import  tkinter as tk
from trading_bot import *
from Configuration import BotConfiguration,URLConfiguration
import configparser
from trading_bot import  *
from threading import Thread
URL = URLConfiguration('./config/bot_config.ini')
getURL = URL.load_url()

bot_config = BotConfiguration('./config/bot_config.ini')
bot_info = bot_config.load()
new_bot = TradingBot(bot_info)
# path = r'/home/arann/pyth0n/BotBian/test.ini'
flag = True

class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.getMode = tk.StringVar()
        self.parent = parent
        self.asd = Thread(target=new_bot.run)
        self.start_count  =  0
        self.ShowLog = Listbox()
        self.menu()
        self.runWindown()
    def runWindown(self):

        self.parent.title("Bot Trading")
        self.pack()

        top_frame = Frame(self)
        top_frame.grid(row=0, column=0, padx=10, pady=5)
        button_frame = Frame(self)
        button_frame.grid(row=1, column=0, padx=10, pady=5)
        self.Showlog= Listbox(top_frame,width=180,height=30, )
        self.Showlog.grid(row=0,column=0)
        scrollBar = Scrollbar(top_frame,orient='vertical',command=self.Showlog.yview)
        self.Showlog['yscrollcommand'] = scrollBar.set
        scrollBar.grid(column=1,row=0,sticky=NS)
        RunBT = Button(button_frame, text="Run", width=10, command=self.start).grid(row=0, column=0 ,padx=10,pady=10)
        StopBT = Button(button_frame, text="Stop", width=10, command=self.stop ).grid(row=0, column=1, pady=10, padx=10)
        Clear_data = Button(button_frame, text="Clear log", width=10, command=self.clear_All_data).grid(row=0, column=2, pady=10, padx=10)

    def Logdata(self,start,data):
        if self.start_count == 100:
            # self.Showlog.delete(0, 1)
            start = 0
        if new_bot.dataloger_enable :
            self.Showlog.insert(start, new_bot.dataloger)
            self.Showlog.see(start)
            self.start_count = self.start_count + 1
            new_bot.dataloger_enable = False
    def clearData(self,start,last):
        self.Showlog.delete(start,last)

    def clear_All_data(self):
        self.Showlog.delete(0,END)

    def start(self):
        new_bot.stop = 0
        t1 = Thread(target=new_bot.run)
        t1.setDaemon(True)
        t1.start()
    def stop(self):
        new_bot.stop = 1
    def menu(self):
        menuBar = Menu(self.parent)
        self.parent.config(menu=menuBar)

        fileMenu = Menu(menuBar)
        fileMenu.add_command(label="Exit", command=self.onExit)
        fileMenu.add_command(label="Configuration", command=self.config)
        menuBar.add_cascade(label="File", menu=fileMenu)


    def onExit(self):
        self.quit()

    def config(self):
        NewWindow(self.parent)

class NewWindow(Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.APIkey = tk.StringVar()
        self.SecretKey = tk.StringVar()
        self.getMode = tk.StringVar()
        self.getName = tk.StringVar()
        self.getURL = tk.StringVar()
        self.config= configparser.RawConfigParser()
        self.Configwd()
    def load_config_GUI(self):
        pass
    def Configwd(self):
        self.title("New Window")
        left_frame = Frame(self)
        left_frame.grid(row=0, column=0, pady=5, padx=5)
        below_left_frame = Frame(self)
        below_left_frame.grid(row=1, column=0, padx=5, pady=5)
        button_frame = Frame(self)
        button_frame.grid(row=2, column=0, padx=10, pady=10)
        lb1 = Label(left_frame, text='Binance API Key:').grid(row=0, column=0)
        entry1 = Entry(left_frame, width=50, textvariable=self.APIkey, )
        entry1.grid(row=0, column=1, pady=5)

        lb2 = Label(left_frame, text='Binance Secret Key:').grid(row=1, column=0)
        entry2 = Entry(left_frame, width=50, textvariable=self.SecretKey)
        entry2.grid(row=1, column=1, pady=5)

        lb3 = Label(below_left_frame, text='Symbol:').grid(row=0, column=0)
        entry3 = Entry(below_left_frame, width=20 ,textvariable= self.getName)
        entry3.grid(row=0, column=1)




        lb4 = Label(below_left_frame,text='URL').grid(row=1,column=0)
        entry4 = Entry(below_left_frame ,width=20,textvariable= self.getURL)
        entry4.grid(row=1, column=1,pady=5)

        lb5= Label(below_left_frame, text='delta_buy:').grid(row=0, column=2)
        entry5 = Entry(below_left_frame, width=20, textvariable=self.getURL)
        entry5.grid(row=0, column=3, pady=5)


        okButton = Button(button_frame, text="OK", width=20, command=self.Getconfig).grid(row=0, column=0, pady=10,padx=10)
        closeButton = Button(button_frame, text="Close", width=20, command=self.destroy).grid(row=0, column=1, pady=10, padx=10)

    def Getconfig(self):
        res = messagebox.askyesno('Confirm', 'Sure :D')
        self.config.read('test.ini')
        if res == True:
            self.config.set('ConfigBot', 'binance_api_key', self.APIkey.get())

            self.config.set('ConfigBot', 'binance_secret_key', self.SecretKey.get())
            self.config.set('URL', 'testnet_url', self.getURL.get())
            self.config.set('ConfigBot', 'symbol', self.getName.get())



            with open('test.ini', 'w') as configfile:
                self.config.write(configfile)
            messagebox.showinfo(' ', ' success')
        else:
            messagebox.showinfo(' ', 'nhap vao moi chay dc')
