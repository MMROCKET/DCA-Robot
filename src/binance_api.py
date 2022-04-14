from datetime import datetime, timezone, timedelta
import hmac
import hashlib
import requests
import json


class BinaceAPI:

    def __init__(self, binance_secret_key, binance_api_key, Testnet_url):
        self.binance_secret_key = binance_secret_key
        self.binance_api_key = binance_api_key
        self.Testnet_url = Testnet_url
        self.hearder = {'X-MBX-APIKEY': self.binance_api_key}

    def create_timestamp(self):
        now = datetime.now(timezone.utc)
        epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
        posix_timestamp_micros = (now - epoch) // timedelta(microseconds=1)
        posix_timestamp_millis = posix_timestamp_micros // 1000
        timestamp = str(posix_timestamp_millis)
        return timestamp

    def account_infor(self, collections):
        signature = hmac.new(self.binance_secret_key.encode(
        ), ("timestamp=" + self.create_timestamp()).encode(), hashlib.sha256).hexdigest()
        param = {
            'timestamp': self.create_timestamp(),
            'signature': signature
        }
        acc_infor = self.Testnet_url + collections
        respone = requests.get(acc_infor, headers=self.hearder, params=param)
        return respone.json(), respone.status_code;

    def get_price(self, collections, symbol):
        get_price = self.Testnet_url + collections
        respone = requests.get(get_price, headers=self.hearder, params={
                               'symbol': str(symbol)}, )
        return respone.json()

    def all_order(self, collections, symbol):
        queryString = "symbol=" + symbol + "&timestamp=" + self.create_timestamp()
        signature = hmac.new(self.binance_secret_key.encode(
        ), queryString.encode(), hashlib.sha256).hexdigest()
        param = {
            'symbol': str(symbol),
            'timestamp': self.create_timestamp(),
            'signature': signature
        }
        trade_buy = self.Testnet_url + collections
        respone = requests.get(trade_buy, headers=self.hearder, params=param)
        return respone.json()

    def trade_order_market(self, collections, symbol, side, quantity):
        queryString = "symbol=" + symbol + "&side=" + side + "&type=MARKET" + \
            "&quantity=" + str(quantity) + "&timestamp=" + \
            self.create_timestamp()
        signature = hmac.new(self.binance_secret_key.encode(
        ), queryString.encode(), hashlib.sha256).hexdigest()
        param = {
            'symbol': str(symbol),
            'side': str(side),
            'type': 'MARKET',
            'quantity': str(quantity),
            'timestamp': self.create_timestamp(),
            'signature': signature
        }
        trade_buy = self.Testnet_url + collections
        respone = requests.post(trade_buy, headers=self.hearder, params=param)
        print(respone.json())
        if respone.status_code == 200:
            return True
        return respone

    def exchange_info(self, collections, symbol):
        get_price = self.Testnet_url + collections
        print(get_price)

        respone = requests.get(get_price, headers=self.hearder, params={
            'symbol': str(symbol)}, )
        status = False
        if respone.status_code == 200:
            status = True
        return status, respone.json()
