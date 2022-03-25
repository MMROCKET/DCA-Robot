from time import time
from unittest import result
from Configuration import *
from BinaceAPI import *
import time
import sys
import os

class TradingBot():
    def __init__(self, bot_info=BotInfo(),):
        self.bot_info = bot_info
        self.is_track_buy = False
        self.is_track_sell = False
        self.lowest_price = 0
        self.avg_price = 0
        self.eth_price = 0
        self.pre_price = 0
        self.binance_api = BinaceAPI(self.bot_info.binance_secret_key, self.bot_info.binance_api_key, self.bot_info.Testnet_url)
        self.stop = 0
        self.dataloger = 'START TRADING BOT'
        self.dataloger_enable = False
    def check_buy(self, price):
        try:
            quantity_per_buy = 0
            if(self.lowest_price == 0):
                self.lowest_price = price
            if(float(price) < float(self.lowest_price)):
                self.lowest_price = price
                self.is_track_buy = True
            if(self.is_track_buy == True):
                if(float(price) > float(self.lowest_price)):
                    delta_condition = ((price - self.lowest_price) / self.lowest_price) * 100
                    print("========================DEBUG - CHECK_BUY: delta = {}".format(delta_condition))
                    if(float(delta_condition) >= float(self.bot_info.delta_buy)):
                        quantity_per_buy = float(self.bot_info.quantity_per_buy)
                        self.is_track_buy = False
                        self.avg_price = (self.avg_price + price) / 2
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
        return quantity_per_buy
    
    def check_sell(self, price):
        try:
            quantity_per_sell = 0
            if(float(price) > float(self.eth_price)):
                self.eth_price = price
            if(self.avg_price == 0):
                self.avg_price = price
            if(float(price) > float(self.avg_price)):
                delta_condition = ((price - self.avg_price) / self.avg_price) * 100
                print("========================DEBUG - CHECK_SELL: delta = {}".format(delta_condition))
                if float(delta_condition) >= float(self.bot_info.profit) + float(self.bot_info.delta_sell):
                    self.is_track_sell = True
                if self.is_track_sell == True:
                    if(float(price) < float(self.eth_price)):
                        delta_condition = ((self.eth_price - price) / price) * 100
                        if(float(delta_condition) >= float(self.bot_info.delta_sell)):
                            quantity_per_sell = float(self.bot_info.quantity_per_sell)
                            self.is_track_sell = False
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
        
        self.pre_price = price
        return quantity_per_sell
        
    def get_time(self):
        named_tuple = time.localtime()  # get struct_time
        time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
        return  time_string
    def run(self,):
        checking_cnt = 60
        self.dataloger = 'START TRADING BOT'
        self.dataloger_enable = True
        while True:
            URL = URLConfiguration('./config/bot_config.ini')
            getURL = URL.load_url()
            symbol = self.bot_info.symbol
            try:
                value = self.binance_api.get_price(getURL.get_price, symbol)
                price = value['price']
                print( "* symbol = {} - price = {}".format(symbol, price))
                # check buy
                quantity = self.check_buy(float(price))
                if(quantity > 0):
                    print("* symbol = {} - price = {} ============================================= action = BUY =================================".format(symbol, price))
                    status = self.binance_api.trade_order_market(getURL.test_oder, symbol, "BUY", quantity)
                    if status == True:
                        self.dataloger = "{} - SUCCESS --> BotVolume Binance -- action: BUY --amount:{} --Price:{} --status: success at {}".format(symbol, quantity, price, self.get_time())
                        self.dataloger_enable = True
                quantity = self.check_sell(float(price))
                if(quantity > 0):
                    print("* symbol = {} - price = {} ============================================= action = SELL ================================".format(symbol, price))
                    self.lowest_price = price
                    status = self.binance_api.trade_order_market(getURL.test_oder, symbol, "SELL", quantity)
                    if status == True :
                        self.dataloger = "{} - SUCCESS --> BotVolume Binance -- action: SELL --amount:{} --Price:{} --status: success   at {}".format(symbol, quantity, price ,self.get_time())
                        self.dataloger_enable = True
                # checking_cnt += 2
                if(checking_cnt >= 60):
                    checking_cnt = 0
                    balances = self.binance_api.account_infor(getURL.acc_infor)["balances"]
                    # USDT_total = 0
                    # BTC_total = 0
                    # for balance in balances:
                    #     if(balance["asset"] == "USDT"):
                    #         USDT_total = balance["free"]
                    #     if(balance["asset"] == "BTC"):
                    #         BTC_total = balance["free"]
                    # print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ USDT_total = {} - BTC_total = {} =================================".format(USDT_total, BTC_total))
                    self.dataloger = "{} - price ={}".format(symbol, price)
                    self.dataloger_enable = True
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                pass
            pass
            time.sleep(1)
            if self.stop == 1:
                self.dataloger = 'STOP TRADING BOT'
                self.dataloger_enable = True
                break