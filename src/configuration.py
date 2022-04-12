import configparser
import os
import sys


class configfile():
    def __init__(self, path):
        self.path_file = path

    def configfile(self):
        config = configparser.ConfigParser()
        config.add_section('ConfigBot')
        config.add_section('URL')
        config.set('URL', 'testnet_url', 'https://testnet.binance.vision/')
        config.set('URL', 'acc_infor', 'api/v3/account')
        config.set('URL', 'get_price', 'api/v3/ticker/price')
        config.set('URL', 'order', 'api/v3/order/test')
        config.set('URL', 'test_oder', '/api/v3/order/test')
        config.set('URL', 'all_oder', 'api/v3/allOrders')

#configURL


class URL():
    acc_infor = ""
    get_price = ""
    Order = ""
    test_oder = ""
    all_oder = ""


class URLConfiguration():
    def __init__(self, path):
        self.path_file = path
        self.url_info = URL()

    def load_url(self):
        config = configparser.ConfigParser()
        config.read(self.path_file)
        self.url_info.acc_infor = config['URL']['acc_infor']
        self.url_info.get_price = config['URL']['get_price']
        self.url_info.Order = config['URL']['Order']
        self.url_info.test_oder = config['URL']['test_oder']
        self.url_info.all_oder = config['URL']['all_oder']
        return self.url_info


# configBot

class BotInfo():
    id = 0
    binance_secret_key = ""
    binance_api_key = ""

    testnet_url = ""
    mainnet_url = ""
    api_url = ""
    symbol = ""

    first_buy_price = 0
    first_buy_quantity = 0
    
    decrease_percent_dca = 0
    increase_percent_dca = 0
    multiple_amount_buy_dca = 0
    
    increase_profit_percent_to_sell = 0
    decrease_profit_percent_to_sell = 0

    max_amount_buy = 0
    quantity_per_sell = 0
    profit = 0

    flag_URl = True


class BotConfiguration():
    def __init__(self, path):
        self.path_file = path
        self.bot_info = BotInfo()
    def load(self):
        try:
            config = configparser.ConfigParser()
            config.read(self.path_file)

            self.bot_info.binance_secret_key = config['ConfigBot']['binance_secret_key']
            self.bot_info.binance_api_key = config['ConfigBot']['binance_api_key']
            self.bot_info.symbol = config['ConfigBot']['symbol']
            self.bot_info.testnet_url = config['ConfigBot']['testnet_url']
            self.bot_info.mainnet_url = config['ConfigBot']['mainnet_url']
            self.bot_info.api_url = config['ConfigBot']['api_url']
            print(self.bot_info.testnet_url)
            self.bot_info.decrease_percent_dca = float(config['CONDITION']['decrease_percent_dca'])
            self.bot_info.increase_percent_dca = float(config['CONDITION']['increase_percent_dca'])
            self.bot_info.multiple_amount_buy_dca = float(config['CONDITION']['multiple_amount_buy_dca'])
            self.bot_info.max_amount_buy = float(config['CONDITION']['max_amount_buy'])
            self.bot_info.increase_profit_percent_to_sell = float(config['CONDITION']['increase_profit_percent_to_sell'])
            self.bot_info.decrease_profit_percent_to_sell = float(config['CONDITION']['decrease_profit_percent_to_sell'])
            self.bot_info.quantity_per_sell = float(config['CONDITION']['quantity_per_sell'])
            self.bot_info.profit = float(config['CONDITION']['profit'])
            # load first buy
            self.bot_info.first_buy_price = float(config['CONDITION']['first_buy_price'])
            self.bot_info.first_buy_quantity = float(config['CONDITION']['first_buy_quantity'])

            return self.bot_info
        except:
            pass

    def save(self):
        try:
            print("BotConfiguration save config")
            config = configparser.ConfigParser()
            config.read(self.path_file)
            config['ConfigBot']['api_url'] = self.bot_info.api_url
            config['ConfigBot']['binance_secret_key'] = self.bot_info.binance_secret_key
            config['ConfigBot']['binance_api_key'] = self.bot_info.binance_api_key
            config['ConfigBot']['symbol'] = self.bot_info.symbol
            config['CONDITION']['decrease_percent_dca'] = str(self.bot_info.decrease_percent_dca)
            config['CONDITION']['increase_percent_dca'] = str(self.bot_info.increase_percent_dca)
            config['CONDITION']['multiple_amount_buy_dca'] = str(self.bot_info.multiple_amount_buy_dca)
            config['CONDITION']['max_amount_buy'] = str(self.bot_info.max_amount_buy)
            config['CONDITION']['increase_profit_percent_to_sell'] = str(self.bot_info.increase_profit_percent_to_sell)
            config['CONDITION']['decrease_profit_percent_to_sell'] = str(self.bot_info.decrease_profit_percent_to_sell)
            config['CONDITION']['quantity_per_sell'] = str(self.bot_info.quantity_per_sell)
            config['CONDITION']['profit'] = str(self.bot_info.profit)
            config['CONDITION']['first_buy_price'] = str(self.bot_info.first_buy_price)
            config['CONDITION']['first_buy_quantity'] = str(self.bot_info.first_buy_quantity)

            with open(self.path_file, 'w') as configfile:
                config.write(configfile)
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

