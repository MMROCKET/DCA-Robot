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
from PIL import Image, ImageTk
class BOTGUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.APIkey = tk.StringVar()
        self.SecretKey = tk.StringVar()
        self.Symbol = tk.StringVar()
        self.getName = tk.StringVar()
        # self.getURL = tk.StringVar()
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
        self.tree = ttk.Treeview()
        self.Combobox = ttk.Combobox()
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
        load = Image.open('config/logo.png')
        ######## logo
        img = load.resize((50, 50), )
        render = ImageTk.PhotoImage(img, )
        img = Label(top_frame, image=render)
        img.image = render
        img.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        ########
        config_frame = Frame(top_frame, relief='raised')
        config_frame.grid(row=2, column=0, pady=5, padx=5, sticky=W)

        sumary = [ 'Sumary:\n',
                    '\n+ Bot will start and do first buy only if price if <== {}\n'.format(self.trading_bot.bot_info.first_buy_price),
                    '\n+ Amount to Buy when start cycle is {}\n'.format(self.trading_bot.bot_info.first_buy_quantity),
                    '\n+ Bot will to strong BUY x {} amount when market price go down {}% and go up {}% after.If price is continuous go down.Bot will boy more to reach limited {}\n'.format(self.trading_bot.bot_info.multiple_amount_buy_dca, self.trading_bot.bot_info.decrease_percent_dca, self.trading_bot.bot_info.increase_percent_dca, self.trading_bot.bot_info.max_amount_buy),
                    '\n+ Bot only sell when market price up >= {} and go down >= {} than actual average price\n'.format(self.trading_bot.bot_info.increase_profit_percent_to_sell, self.trading_bot.bot_info.decrease_profit_percent_to_sell),
                    '\n+ So profit always >= 1 % forever!\n'
        ]


        sumary_frame = Frame(top_frame,)
        sumary_frame.grid(row=1, column=1, pady=5, padx=5,rowspan=2)
        Showlog =Text(sumary_frame, width=30, height=30, wrap='word')
        Showlog.grid(row=0, column=0,)
        for i in range(len(sumary)):
            print(sumary[i])
            Showlog.insert(tk.END,sumary[i])
        Showlog.config(state=DISABLED)

        # lable first buy price
        lb = Label(config_frame, text='Price <= (usd)').grid(row=0, column=1,sticky=W)
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
        lb = Label(config_frame, text='Step 1: price decrease (%)').grid(row=2, column=1,sticky=W)
        lb = Label(config_frame, text='Step 2: and price up (%)').grid(row=2, column=3,sticky=W)
        lb = Label(config_frame, text='Multiple amount to buy').grid(row=2, column=5,sticky=W)

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
        lb = Label(config_frame, text='Step 1: price increase (%)').grid(row=6, column=1,sticky=W)
        lb = Label(config_frame, text='Step 2: and price down (%)').grid(row=6, column=3,sticky=W)
        lb = Label(config_frame, text='Sell When').grid(row=7, column=0,sticky=W)
        entry = Entry(config_frame, width=30, textvariable=self.increase_profit_percent_to_sell)
        entry.grid(row=7, column=1, pady=5,sticky=W)
        entry.insert(0, self.bot_info.increase_profit_percent_to_sell)
        entry = Entry(config_frame, width=30, textvariable=self.decrease_profit_percent_to_sell)
        entry.grid(row=7, column=3, pady=7,sticky=W)
        entry.insert(0, self.bot_info.decrease_profit_percent_to_sell)

        new_frame = Frame(top_frame)
        new_frame.grid(row=1, column=0,sticky=W)

        # Binance API Key
        lb = Label(new_frame, text='Binance API Key:').grid(row=0, column=0,sticky=W)
        entry = Entry(new_frame, width=30, textvariable=self.APIkey)
        entry.grid(row=0, column=1, pady=10, sticky=W)
        entry.insert(0, self.bot_info.binance_api_key)
        lb = Label(new_frame, text='       ').grid(row=1, column=4, sticky=W)

        # Binance Secret Key
        lb = Label(new_frame, text='Binance Secret Key:').grid(row=1, column=0,sticky=W)
        entry = Entry(new_frame, width=30, textvariable=self.SecretKey)
        entry.grid(row=1, column=1, pady=10,)
        entry.insert(0, self.bot_info.binance_secret_key)

        # Binance URL
        lb = Label(new_frame, text='URL:').grid(row=0, column=2 ,)
        self.Combobox = ttk.Combobox(new_frame, width=27,)
        self.Combobox.grid(row=0, column=3, pady=5, )
        self.Combobox['values'] = ('Testnet', 'Mainnet')
        self.Combobox['state'] = 'readonly'
        self.Combobox.current(0)
        # self.Combobox.bind('<<ComboboxSelected>>', self.getURL)
        # Binance Symbol
        lb = Label(new_frame, text='Symbol:').grid(row=1, column=2,)
        entry = Entry(new_frame, width=30, textvariable=self.Symbol)
        entry.grid(row=1, column=3, pady=5, sticky=W)
        entry.insert(0, self.bot_info.symbol)

        # Check Key
        button_stop = Button(new_frame, text="Check Account", width=15, command=self.Check_key)
        button_stop.grid(row=1, column=5, pady=5,sticky=W )

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
                    'total_buy', 'avg_price', 'status', 'total_sell', 'profit', 'ROI', 'action')


        self.tree = ttk.Treeview(config_frame, columns=columns, show='headings',)
        self.tree['columns'] = ('cycle', 'current_bot',
                                'total_buy', 'avg_price', 'status', 'total_sell', 'profit', 'ROI', 'action')


        # format our column
        self.tree.column("#0", width=10,  stretch=NO)
        self.tree.column("cycle", anchor=CENTER, width=80)
        self.tree.column("current_bot", anchor=CENTER, width=100)
        # self.tree.column("config_info", anchor=CENTER, width=80)
        self.tree.column("total_buy", anchor=CENTER, width=100)
        self.tree.column("avg_price", anchor=CENTER, width=100)
        self.tree.column("status", anchor=CENTER, width=80)
        self.tree.column("total_sell", anchor=CENTER, width=80)
        self.tree.column("profit", anchor=CENTER, width=80)
        self.tree.column("ROI", anchor=CENTER, width=80)
        self.tree.column("action", anchor=CENTER, width=80)

        #Create Headings
        self.tree.heading("#0", text="", anchor=CENTER)
        self.tree.heading("cycle", text="CYCLE", anchor=CENTER)
        self.tree.heading("current_bot", text="CURRENT BOT", anchor=CENTER)
        # self.tree.heading("config_info", text="CONFIG INFO", anchor=CENTER)
        self.tree.heading("total_buy", text="TOTAL BUY", anchor=CENTER)
        self.tree.heading("avg_price", text="AVG PRICE", anchor=CENTER)
        self.tree.heading("status", text="STATUS", anchor=CENTER)
        self.tree.heading("total_sell", text="TOTAL", anchor=CENTER)
        self.tree.heading("profit", text="PROFIT", anchor=CENTER)
        self.tree.heading("ROI", text="ROI", anchor=CENTER)
        self.tree.heading("action", text="ACTION", anchor=CENTER)

        #### scrollBarTree
        scrollBar = Scrollbar(config_frame, command=self.tree.yview)
        self.tree['yscrollcommand'] = scrollBar.set
        scrollBar.grid(row=11, column=6,sticky=[ E,NS])
        scrollBar.config(command=self.tree.yview)
        # tree.insert(parent='', index='end', iid=0, text='',
        #                values=('1', 'Ninja', '101', 'Oklahoma', 'Moore'))
        self.tree.grid(row=11, column=0, padx=0, pady=1, columnspan=6)

        #
        log_frame = Frame(self)
        log_frame.grid(row=2, column=0, pady=10, padx=10,sticky=W)
        lb = Label(log_frame, text='Log information:').grid( row=0, column=0, sticky=W)

        self.ShowLog = Listbox(log_frame, width=150, height=15, )
        self.ShowLog.grid(row=1, column=0,columnspan=2 )
        scrollBar = Scrollbar(log_frame, command=self.ShowLog.yview)
        self.ShowLog['yscrollcommand'] = scrollBar.set
        scrollBar.grid(column=1, row=1,sticky=[NS, E])

        bt = Button(log_frame, text='Clear Log', command=self.clear_All_data).grid(row=2, column=1, sticky=SE)

    # def getURL(self):
    #     if self.Combobox.get() == 'Testnet':
    #         self.bot_info.flag_URl = True
    #     else:
    #         self.bot_info.flag_URl = False
    def Check_key(self):
        m_binance_api_key = self.APIkey.get()
        m_binance_secret_key = self.SecretKey.get()
        if self.Combobox.get() == 'Mainnet':
            self.trading_bot.bot_info.api_url = self.trading_bot.bot_info.mainnet_url
            print(self.trading_bot.bot_info.api_url)
        else:
            self.trading_bot.bot_info.api_url = self.trading_bot.bot_info.testnet_url
            print(self.trading_bot.bot_info.api_url)
        if(self.trading_bot.check_account(m_binance_secret_key, m_binance_api_key)):
            messagebox.showinfo('Check Account', 'Success!')
        else:
            messagebox.showerror('Check Account', 'Something went wrong!')
    def TalbeTradingInfor(self):
        for key in self.trading_bot.trading_dict:
            trading_infor = self.trading_bot.trading_dict[key]
            if self.tree.exists(str(key)) == True:
                self.tree.item(item=str(key),
                               values=(trading_infor.cycle, trading_infor.symbol, trading_infor.Config_infor, trading_infor.total_buy, trading_infor.avg_price, trading_infor.status, trading_infor.total, trading_infor.profit, trading_infor.roi, trading_infor.action))
            else:
                self.tree.insert(parent='', index='end', text='',iid=str(key),
                               values=(trading_infor.cycle, trading_infor.symbol,trading_infor.Config_infor, trading_infor.total_buy, trading_infor.avg_price, trading_infor.status, trading_infor.total, trading_infor.profit, trading_infor.roi, trading_infor.action))


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
        print(self.Combobox.get())
        if self.Combobox.get() == 'Mainnet':
            self.trading_bot.bot_info.api_url = self.trading_bot.bot_info.mainnet_url
            print(self.trading_bot.bot_info.api_url)
        else:
            self.trading_bot.bot_info.api_url = self.trading_bot.bot_info.testnet_url
            print(self.trading_bot.bot_info.api_url)
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

        print("SecretKey: {}".format(self.SecretKey.get()))
        if(self.trading_bot.is_running == False):
            self.trading_bot.stop = False
            self.trading_bot.is_first = True
            self.trading_bot.update_config()
            t1 = Thread(target=self.trading_bot.run)
            t1.setDaemon(True)
            t1.start()

    def action_stop(self):
        print("stop BOT")
        self.trading_bot.stop = True
        print(self.trading_bot.stop)


def log_task(app):
    while(1):
        app.Logdata()
        app.TalbeTradingInfor()
        time.sleep(0.5)
if __name__ == '__main__':
    root = Tk()
    app = BOTGUI(root)
    #
    t2 = Thread(target=log_task, args=(app,))

    t2.start()

    app.mainloop()
