from BinaceAPI import BinaceAPI
from Configuration import BotConfiguration,URLConfiguration,configfile
import sys

from tkinter import *
from  threading import  Thread

from GUI import *
from time import strftime
import time

URL = URLConfiguration('./config/bot_config.ini')
getURL = URL.load_url()


bot_config = BotConfiguration('./config/bot_config.ini')
get_info = bot_config.load()

header = {'X-MBX-APIKEY': get_info.binance_api_key}
bot = BinaceAPI(get_info.binance_secret_key, get_info.binance_api_key, getURL.Testnet_url)

root = Tk()

app = Example(root)
def get_price():
    start=0
    while True:
        time_string = strftime('%H:%M:%S %p')
        getUSD = bot.get_price(getURL.get_price, 'BTCUSDT')
        data = time_string + " " + getUSD['price']

        app.Logdata(start, data)
        # start = start + 1
        # if start == 100 :
        #     app.clearData(0,100)
        #     start=0
        time.sleep(0.5)

if __name__ == '__main__':



    # root = Tk()
    #
    # app = Example(root)
    t2  = Thread( target= get_price,)
    t2.start()
    root.mainloop()




# getUSD = bot.get_price(getURL.get_price, 'BTCUSDT')
# print(getUSD['price'])