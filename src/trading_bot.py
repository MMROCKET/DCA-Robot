from time import time
from unittest import result
from configuration import *
from binance_api import *
import time


class TradingBot():
    def __init__(self, bot_info = BotInfo()):
        self.bot_info = bot_info
        self.is_track_buy = False
        self.is_track_sell = False
        self.lowest_price = 0
        self.avg_price = 0
        self.eth_price = 0
        self.pre_price = 0
        self.binance_api = BinaceAPI(self.bot_info.binance_secret_key, self.bot_info.binance_api_key, self.bot_info.Testnet_url)

    def check_buy(self, price):
        quantity_per_buy = 0
        if(self.lowest_price == 0):
            self.lowest_price = price
        if(price < self.lowest_price):
            self.lowest_price = price
            self.is_track_buy = True
        if(self.is_track_buy == True):
            if(price > self.lowest_price):
                delta_condition = ((price - self.lowest_price) / self.lowest_price) * 100
                print("========================DEBUG - CHECK_BUY: delta = {}".format(delta_condition))
                if(delta_condition >= self.bot_info.delta_buy):
                    quantity_per_buy = self.bot_info.quantity_per_buy
                    self.is_track_buy = False
                    self.avg_price = (self.avg_price + price) / 2
        return quantity_per_buy
    
    def check_sell(self, price):
        quantity_per_sell = 0
        if(price > self.eth_price):
            self.eth_price = price
        if(self.avg_price == 0):
            self.avg_price = price
        if(price > self.avg_price):
            delta_condition = ((price - self.avg_price) / self.avg_price) * 100
            print("========================DEBUG - CHECK_SELL: delta = {}".format(delta_condition))
            if delta_condition >= self.bot_info.profit + self.bot_info.delta_sell:
                self.is_track_sell = True
            if self.is_track_sell == True:
                if(price < self.eth_price):
                    delta_condition = ((self.eth_price - price) / price) * 100
                    if(delta_condition >= self.bot_info.delta_sell):
                        quantity_per_sell = self.bot_info.quantity_per_sell
                        self.is_track_sell = False
        
        self.pre_price = price
        return quantity_per_sell
        
    
    def run(self):
        checking_cnt = 10
        while True:
            time.sleep(1)
            URL = URLConfiguration('./config/bot_config.ini')
            getURL = URL.load_url()
            symbol = self.bot_info.symbol
            try:
                value = self.binance_api.get_price(getURL.get_price, symbol)
                price = value['price']
                print("* symbol = {} - price = {}".format(symbol, price))
                # check buy
                if(self.check_buy(float(price))):
                    print("* symbol = {} - price = {} ============================================= action = BUY =================================".format(symbol, price))
                    print(self.binance_api.trade_order_market(getURL.test_oder, symbol, "BUY", 0.001))
                if(self.check_sell(float(price))):
                    print("* symbol = {} - price = {} ============================================= action = SELL ================================".format(symbol, price))
                    print(self.binance_api.trade_order_market(getURL.test_oder, symbol, "SELL", 0.001))
                checking_cnt += 1
                if(checking_cnt >= 10):
                    checking_cnt = 0
                    balances = self.binance_api.account_infor(getURL.acc_infor)["balances"]
                    USDT_total = 0
                    BTC_total = 0
                    for balance in balances:
                        if(balance["asset"] == "USDT"):
                            USDT_total = balance["free"]
                        if(balance["asset"] == "BTC"):
                            BTC_total = balance["free"]
                    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ USDT_total = {} - BTC_total = {} =================================".format(USDT_total, BTC_total))
            except:
                pass
            pass