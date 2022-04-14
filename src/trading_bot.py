from itertools import cycle
from time import sleep, time
from unittest import result
from configuration import *
from binance_api import *
import time
import sys
import os


class TradingInfo():
    cycle = 0
    symbol = ""
    Config_infor = ""
    total_buy = 0
    avg_price = 0
    status = "RUNNING"
    total = 0
    profit = 0
    roi = 0
    action = ""

class TradingBot():
    def __init__(self, bot_info=BotInfo(), ):
        self.bot_info = bot_info
        self.check_buy_step = float(0)
        self.is_track_buy = False
        self.is_track_sell = False
        self.lowest_price = float(0)
        self.avg_price = float(0)
        self.eth_price = float(0)
        self.pre_price = float(0)
        self.binance_api = BinaceAPI(self.bot_info.binance_secret_key, self.bot_info.binance_api_key,
                                     self.bot_info.api_url)
        self.stop = 0
        self.is_running = False
        self.dataloger = 'START TRADING BOT'
        self.dataloger_enable = False

        self.is_first = True
        self.old_amount_buy = 0

        self.trading_info = TradingInfo()
        self.cycle_num = 0
        self.trading_dict = {}

    def get_time(self):
        named_tuple = time.localtime()  # get struct_time
        time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
        return time_string

    def do_buy(self, test_oder, symbol, price, quantity):
        print("test_oder: {}".format(test_oder))
        status = self.binance_api.trade_order_market(test_oder, symbol, "BUY", float(quantity))
        if status == True:
            self.trading_info.total_buy += quantity
            self.trading_dict[self.cycle_num] = self.trading_info
            self.dataloger = "{} - SUCCESS --> BotVolume Binance -- action: BUY --amount:{} --Price:{} --status: success at {}".format(
                symbol, quantity, price, self.get_time())
            self.dataloger_enable = True
            self.old_amount_buy = quantity
        return status

    def do_sell(self, getURL, symbol, price, quantity):
        print("[SELL} : * symbol = {} - price = {}".format(symbol, price))
        self.lowest_price = price
        status = self.binance_api.trade_order_market(getURL.test_oder, symbol, "SELL", quantity)
        if status == True:
            self.dataloger = "{} - SUCCESS --> BotVolume Binance -- action: SELL --amount:{} --Price:{} --status: success   at {}".format(
                symbol, quantity, price, self.get_time())
            self.dataloger_enable = True
            self.eth_price = price

    def first_trading(self, getURL, symbol, cur_price):
        if float(cur_price) <= float(self.bot_info.first_buy_price):
            print("[FIRST BUY] :cur_price = {} - price_to_buy = {}".format(cur_price, self.bot_info.first_buy_price))
            status = self.do_buy(getURL.test_oder, symbol, float(cur_price), float(self.bot_info.first_buy_quantity))
            if status == True:
                print("Do First Buy Success")
                self.is_first = False
                self.lowest_price = cur_price
                self.eth_price = cur_price
                self.avg_price = cur_price

    def check_buy(self, price):
        try:
            amount_buy = 0
            if (self.lowest_price == 0):
                self.lowest_price = price

            # check decrease value percent (step 1)
            if (float(price) < float(self.lowest_price)):
                decrease_percent_dca = float(((self.lowest_price - price) / price) * 100)
                if (float(decrease_percent_dca) >= float(self.bot_info.decrease_percent_dca)):
                    self.lowest_price = price
                    self.is_track_buy = True
            # check increase value percent after decrease before (step 2)
            if (self.is_track_buy == True):
                if (float(price) > float(self.lowest_price)):
                    increase_percent_dca = ((price - self.lowest_price) / self.lowest_price) * 100
                    if (float(increase_percent_dca) >= float(self.bot_info.increase_percent_dca)):
                        amount_buy = float(self.bot_info.multiple_amount_buy_dca) * float(self.old_amount_buy)
                        if (amount_buy > float(self.bot_info.max_amount_buy)):
                            amount_buy = float(self.bot_info.max_amount_buy)
                        self.is_track_buy = False
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
        return amount_buy

    def check_sell(self, price):
        try:
            quantity_per_sell = 0
            # check current value greater than old max price
            if (float(price) > float(self.eth_price)):
                self.eth_price = price

            if (float(price) > float(self.avg_price)):
                increase_profit_percent_to_sell = float(((price - float(self.avg_price)) / float(self.avg_price)) * 100)
                # tracking_condition
                if float(increase_profit_percent_to_sell) >= float(self.bot_info.increase_profit_percent_to_sell):
                    self.is_track_sell = True

                if self.is_track_sell == True:
                    if (float(price) < float(self.eth_price)):  # if market inverse price
                        decrease_profit_percent_to_sell = ((self.eth_price - price) / price) * 100
                        if (float(decrease_profit_percent_to_sell) >= float(
                                self.bot_info.decrease_profit_percent_to_sell)):
                            quantity_per_sell = float(self.bot_info.quantity_per_sell)
                            self.is_track_sell = False
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

        return quantity_per_sell

    def save_config(self):
        # try:
        if True:
            print("[SAVE CONFIG] : {}".format(self.bot_info.multiple_amount_buy_dca))
            configuration = BotConfiguration("./config/bot_config.ini")
            configuration.bot_info = self.bot_info
            configuration.save()
            print("[SAVE CONFIG] : SUCCESS")
            pass
        # except:
        #     exc_type, exc_obj, exc_tb = sys.exc_info()
        #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        #     print(exc_type, fname, exc_tb.tb_lineno)

    def run(self, ):
        self.update_config()
        self.is_running = True
        checking_cnt = 60
        if(self.check_account(self.bot_info.binance_secret_key, self.bot_info.binance_api_key)):
            self.dataloger = 'START TRADING BOT - ACCOUNT INFORMATION IS VALID! ---- ' + self.bot_info.api_url
            self.dataloger_enable = True
        else:
            self.dataloger = 'STOP TRADING BOT - THERE IS SOMETHING WRONG WITH THE ACCOUNT INFORMATION! ---- ' + self.bot_info.api_url
            self.dataloger_enable = True
            self.is_running = False
            return 0
        sleep(2)
        self.trading_info = TradingInfo()
        self.cycle_num += 1

        self.trading_info.cycle = self.cycle_num
        self.trading_info.status = "RUNNING"
        self.trading_info.symbol = self.bot_info.symbol
        self.trading_dict[self.cycle_num] = self.trading_info

        URL = URLConfiguration('./config/bot_config.ini')
        getURL = URL.load_url()
        while True:
            if self.stop == 1:
                self.dataloger = 'STOP TRADING BOT'
                self.dataloger_enable = True
                break
            
            symbol = self.bot_info.symbol
            try:
                value = self.binance_api.get_price(getURL.get_price, symbol)
                price = float(value['price'])
                print("[Real Time]: * symbol = {} - price = {}".format(symbol, price))

                # check first trading
                if (self.is_first == True):
                    self.first_trading(getURL, symbol, price)
                    continue

                # check buy
                quantity = float(self.check_buy(float(price)))
                if (float(quantity) > 0):
                    if(self.do_buy(getURL.test_oder, symbol, float(price), quantity) == True):
                        self.avg_price = (self.avg_price + price) / 2

                # check sell
                quantity = float(self.check_sell(float(price)))
                if (float(quantity) > 0):
                    self.do_sell(getURL.test_oder, symbol, price, quantity)

                checking_cnt += 1
                if (checking_cnt >= 60):
                    checking_cnt = 0
                    balances = self.binance_api.account_infor(getURL.acc_infor)["balances"]
                    USDT_total = 0
                    BTC_total = 0
                    # for balance in balances:
                    #     if(balance["asset"] == "USDT"):
                    #         USDT_total = balance["free"]
                    #     if(balance["asset"] == "BTC"):
                    #         BTC_total = balance["free"]
                    # print("+++++++++USDT_total = {} - BTC_total = {} =================================".format(USDT_total, BTC_total))
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                pass
            pass
            time.sleep(1)
            self.trading_info.avg_price = self.avg_price

        self.trading_info.status = "STOP"
        self.trading_dict[self.cycle_num] = self.trading_info
        self.is_running = False

    def check_account(self, m_binance_secret_key, m_binance_api_key):
        URL = URLConfiguration('./config/bot_config.ini')
        getURL = URL.load_url()
        m_binance_api = BinaceAPI(m_binance_secret_key, m_binance_api_key, self.bot_info.api_url)
        print(self.bot_info.api_url)
        balances, status_code = m_binance_api.account_infor(getURL.acc_infor)
        if(status_code == 200):
            return True
        print(balances)
        print(status_code)

        return False

    def update_config(self):
        self.binance_api = BinaceAPI(self.bot_info.binance_secret_key, self.bot_info.binance_api_key,
                                     self.bot_info.api_url)

# bot_config = BotConfiguration('./config/bot_config.ini')
# bot_info = bot_config.load()
# trading_bot = TradingBot(bot_info)
# trading_bot.check_account("abc", "123")
