from tkinter import messagebox
from tkinter import *
from tkinter import ttk
from tkinter import Label
import tkinter as tk
from trading_bot import *
from configuration import BotConfiguration, URLConfiguration
import configparser
from trading_bot import *
from threading import Thread
import time

class BOTGUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.APIkey = tk.StringVar()
        self.SecretKey = tk.StringVar()
        self.Symbol = tk.StringVar()
        self.getName = tk.StringVar()
        self.getURL = tk.StringVar()
        self.getMode = tk.StringVar()
        self.parent = parent
        self.start_count = 0
        self.ShowLog = Listbox()

        self.firstBuyPrice = tk.StringVar()
        self.first_buy_quantity = tk.StringVar()
        self.decrease_percent_dca = tk.StringVar()
        self.increase_percent_dca = tk.StringVar()
        self.multiple_amount_buy_dca = tk.StringVar()
        self.max_amount_buy = tk.StringVar()
        self.increase_profit_percent_to_sell = tk.StringVar()
        self.decrease_profit_percent_to_sell = tk.StringVar()

        # logger
        self.logLine = 0

        # Bot
        bot_config = BotConfiguration('./config/bot_config.ini')
        self.bot_info = bot_config.load()
        self.trading_bot = TradingBot(self.bot_info)
        self.runWindown()

    def runWindown(self):
        self.parent.title("Bot Trading")
        self.pack(anchor="e")
        
        top_frame = Frame(self)
        top_frame.grid(row=0, column=0, pady=5, padx=5)

        config_frame = Frame(top_frame)
        config_frame.grid(row=0, column=0, pady=5, padx=5,sticky=W)

        sumary = [ 'Sumary:\n',
                    '\n+ Bot will start and do first buy only if price if <== {}\n',
                    '\n+ Amount to Buy when start cycle is {}\n',
                    '\n+ Bot will to strong BUY x {} amount when market price go down{}% and go up{}% after.If price is continuous go down.Bot will boy more to reach limited{}\n',
                    '\n+ Bot only sell when market price up >= {} and go down >= {} than actual average price\n',
                    '\n+ So profit always >= 1 % forever!\n'
        ]


        sumary_frame = Frame(top_frame,)
        sumary_frame.grid(row=0, column=1, pady=5, padx=5)
        Showlog =Text(sumary_frame, width=30, height=30, wrap='word')
        Showlog.grid(row=0, column=0,)
        for i in range(len(sumary)):
            print(sumary[i])
            Showlog.insert(tk.END,sumary[i])
        Showlog.config(state=DISABLED)

        # lable first buy price
        lb = Label(config_frame, text='price <= (usd)').grid(row=0, column=1,sticky=W)
        lb = Label(config_frame, text='       ').grid(row=0, column=2, sticky=W)
        
        # lable amount first buy
        lb = Label(config_frame, text='Amount buy at 1st').grid(row=0, column=3, sticky=W)
        lb = Label(config_frame, text='       ').grid(row=0, column=4, sticky=W)

        # entry first buy price
        lb = Label(config_frame, text='1st Buy Price').grid(row=1, column=0,sticky=W)
        entry = Entry(config_frame, width=30, textvariable=self.firstBuyPrice)
        entry.grid(row=1, column=1, pady=5 ,sticky=W)
        entry.insert(0, self.bot_info.first_buy_price)

        # entry amount first buy
        entry = Entry(config_frame, width=30, textvariable=self.first_buy_quantity)
        entry.grid(row=1, column=3, pady=5,sticky=W)
        entry.insert(0, self.bot_info.first_buy_quantity)
        
        #label dca
        lb = Label(config_frame, text='step 1: price decrease (%)').grid(row=2, column=1,sticky=W)
        lb = Label(config_frame, text='step 2: and price up (%)').grid(row=2, column=3,sticky=W)
        lb = Label(config_frame, text='multiple amount to buy').grid(row=2, column=5,sticky=W)

        # DCA
        lb = Label(config_frame, text='DCA when').grid(row=3, column=0,sticky=W)
        entry = Entry(config_frame, width=30, textvariable=self.decrease_percent_dca)
        entry.grid(row=3, column=1, pady=5, sticky=W)
        entry.insert(0, self.bot_info.decrease_percent_dca)
        entry = Entry(config_frame, width=30, textvariable=self.increase_percent_dca)
        entry.grid(row=3, column=3, pady=5, sticky=W)
        entry.insert(0, self.bot_info.increase_percent_dca)
        entry = Entry(config_frame, width=30, textvariable=self.multiple_amount_buy_dca)
        entry.grid(row=3, column=5, pady=5, sticky=W)
        entry.insert(0, self.bot_info.multiple_amount_buy_dca)

        lb = Label(config_frame, text='Max amount per cycle to buy').grid(row=4, column=1,sticky=W)
        lb = Label(config_frame, text='Max Buy').grid(row=5, column=0,sticky=W)
        entry = Entry(config_frame, width=30, textvariable=self.max_amount_buy)
        entry.grid(row=5, column=1, pady=5, sticky=W)
        entry.insert(0, self.bot_info.max_amount_buy)

        #sell
        lb = Label(config_frame, text='step 1: price increase (%)').grid(row=6, column=1,sticky=W)
        lb = Label(config_frame, text='step 2: and price down (%)').grid(row=6, column=3,sticky=W)
        lb = Label(config_frame, text='Sell When').grid(row=7, column=0,sticky=W)
        entry = Entry(config_frame, width=30, textvariable=self.increase_profit_percent_to_sell)
        entry.grid(row=7, column=1, pady=5,sticky=W)
        entry.insert(0, self.bot_info.increase_profit_percent_to_sell)
        entry = Entry(config_frame, width=30, textvariable=self.decrease_profit_percent_to_sell)
        entry.grid(row=7, column=3, pady=7,sticky=W)
        entry.insert(0, self.bot_info.decrease_profit_percent_to_sell)

        # Binance API Key
        lb = Label(config_frame, text='Binance API Key:').grid(row=9, column=0,sticky=W)
        entry = Entry(config_frame, width=30, textvariable=self.APIkey)
        entry.grid(row=9, column=1, pady=10, sticky=W)
        entry.insert(0, self.bot_info.binance_api_key)
        
        # Binance Secret Key
        lb = Label(config_frame, text='Binance Secret Key:').grid(row=10, column=0,sticky=W)
        entry = Entry(config_frame, width=30, textvariable=self.SecretKey)
        entry.grid(row=10, column=1, pady=10, sticky=W)
        entry.insert(0, self.bot_info.binance_secret_key)

        # Binance URL
        lb = Label(config_frame, text='URL:').grid(row=9, column=2 , sticky=W)
        entry = Entry(config_frame, width=30, textvariable=self.getURL)
        entry.grid(row=9, column=3, pady=5, sticky=W)
        entry.insert(0, self.bot_info.Testnet_url)

        # Binance Symbol
        lb = Label(config_frame, text='Symbol:').grid(row=10, column=2, sticky=W)
        entry = Entry(config_frame, width=30, textvariable=self.Symbol)
        entry.grid(row=10, column=3, pady=5, sticky=W)
        entry.insert(0, self.bot_info.symbol)

        # midd_frame = Frame(self)
        # midd_frame.grid(row=1, column=0, pady=5, padx=5, sticky=W)
        #
        action_frame = Frame(sumary_frame)
        action_frame.grid(row=1, column=0, pady=1, padx=20, sticky=W)
        button_run = Button(action_frame, text="Run", width=15, command=self.action_run)
        button_run.grid(row=0, column=1, pady=5,)
        button_stop = Button(action_frame, text="Stop", width=15, command=self.action_stop)
        button_stop.grid(row=0, column=2, pady=5,)
        # #
        # bot_info_frame = Frame(midd_frame)
        # bot_info_frame.grid(row=0, column=0, pady=10, padx=20, sticky=W)


        total_rows = 2
        total_columns = 10

        columns = ('cycle', 'current_bot',
                   'config_info', 'total_buy', 'avg_price', 'status', 'total_sell', 'profit', 'ROI', 'action')


        tree = ttk.Treeview(config_frame, columns=columns, show='headings')
        tree['columns'] = ('cycle', 'current_bot',
                           'config_info', 'total_buy', 'avg_price', 'status', 'total_sell', 'profit', 'ROI', 'action')


        # format our column
        tree.column("#0", width=10,  stretch=NO)
        tree.column("cycle", anchor=CENTER, width=80)
        tree.column("current_bot", anchor=CENTER, width=120)
        tree.column("config_info", anchor=CENTER, width=120)
        tree.column("total_buy", anchor=CENTER, width=80)
        tree.column("avg_price", anchor=CENTER, width=80)
        tree.column("status", anchor=CENTER, width=80)
        tree.column("total_sell", anchor=CENTER, width=80)
        tree.column("profit", anchor=CENTER, width=80)
        tree.column("ROI", anchor=CENTER, width=80)
        tree.column("action", anchor=CENTER, width=80)

        #Create Headings
        tree.heading("#0", text="", anchor=CENTER)
        tree.heading("cycle", text="Cycle", anchor=CENTER)
        tree.heading("current_bot", text="Current Bot", anchor=CENTER)
        tree.heading("config_info", text="Config info", anchor=CENTER)
        tree.heading("total_buy", text="total BUY", anchor=CENTER)
        tree.heading("avg_price", text="Avg Price", anchor=CENTER)
        tree.heading("status", text="status", anchor=CENTER)
        tree.heading("total_sell", text="total", anchor=CENTER)
        tree.heading("profit", text="profit", anchor=CENTER)
        tree.heading("ROI", text="ROI", anchor=CENTER)
        tree.heading("action", text="action", anchor=CENTER)

        # tree.insert(parent='', index='end', iid=0, text='',
        #                values=('1', 'Ninja', '101', 'Oklahoma', 'Moore'))
        tree.grid(row=11, column=0, padx=0, pady=1,columnspan=6)

        #
        log_frame = Frame(self)
        log_frame.grid(row=2, column=0, pady=10, padx=10,sticky=W)
        lb = Label(log_frame, text='Log information:').grid( row=0, column=0, sticky=W)

        self.ShowLog = Listbox(log_frame, width=150, height=15, )
        self.ShowLog.grid(row=1, column=0,columnspan=2 )
        scrollBar = Scrollbar(log_frame, command=self.ShowLog.yview)
        self.ShowLog['yscrollcommand'] = scrollBar.set
        scrollBar.grid(column=1, row=1,sticky=[NS, E])

        bt = Button(log_frame, text='Clear Log').grid(row=2, column=1, sticky=SE)

    def Logdata(self):
        if self.trading_bot.dataloger_enable :
            self.ShowLog.insert(self.logLine, self.trading_bot.dataloger)
            self.ShowLog.see(self.logLine)
            self.start_count = self.start_count + 1
            self.trading_bot.dataloger_enable = False
            self.logLine = self.logLine + 1

    def clearData(self,line,last):
        self.ShowLog.delete(line,last)

    def clear_All_data(self):
        self.ShowLog.delete(0,END)

    def action_run(self):
        # save config
        self.trading_bot.bot_info.binance_api_key = self.APIkey.get()
        self.trading_bot.bot_info.binance_secret_key = self.SecretKey.get()
        self.trading_bot.bot_info.Testnet_url = self.getURL.get()
        self.trading_bot.bot_info.symbol = self.Symbol.get()
        self.trading_bot.bot_info.first_buy_price = self.firstBuyPrice.get()
        self.trading_bot.bot_info.first_buy_quantity = self.first_buy_quantity.get()
        self.trading_bot.bot_info.decrease_percent_dca = self.decrease_percent_dca.get()
        self.trading_bot.bot_info.increase_percent_dca = self.increase_percent_dca.get()
        self.trading_bot.bot_info.multiple_amount_buy_dca = self.multiple_amount_buy_dca.get()
        self.trading_bot.bot_info.max_amount_buy = self.max_amount_buy.get()
        self.trading_bot.bot_info.increase_profit_percent_to_sell = self.increase_profit_percent_to_sell.get()
        self.trading_bot.bot_info.decrease_profit_percent_to_sell = self.decrease_profit_percent_to_sell.get()
        self.trading_bot.save_config()
        # print("run BOT")

        # print("SecretKey: {}".format(self.SecretKey.get()))
        if(self.trading_bot.is_running == False):
            self.trading_bot.stop = False
            self.trading_bot.is_first = True
            t1 = Thread(target=self.trading_bot.run)
            t1.setDaemon(True)
            t1.start()

    def action_stop(self):
        print("stop BOT")
        self.trading_bot.stop = True


def log_task(app):
    while(1):
        app.Logdata()
        time.sleep(1)

if __name__ == '__main__':
    root = Tk()
    app = BOTGUI(root)
    
    t2 = Thread(target=log_task, args=(app,))
    t2.start()

    app.mainloop()
