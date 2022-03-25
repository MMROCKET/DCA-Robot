import configparser


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
    Testnet_url = ""
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
        self.url_info.Testnet_url = config['URL']['Testnet_url']
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

    Testnet_url = ""
    symbol = ""

    delta_buy = 0
    quantity_per_buy = 0
    delta_sell = 0
    quantity_per_sell = 0
    profit = 0


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
            self.bot_info.Testnet_url = config['ConfigBot']['testnet_url']
            # load condition
            self.bot_info.delta_buy = config['CONDITION']['delta_buy']
            self.bot_info.quantity_per_buy = config['CONDITION']['quantity_per_buy']
            self.bot_info.delta_sell = config['CONDITION']['delta_sell']
            self.bot_info.quantity_per_sell = config['CONDITION']['quantity_per_sell']
            self.bot_info.profit = config['CONDITION']['profit']
            return self.bot_info
        except:
            pass