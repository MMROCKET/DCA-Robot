from hashlib import new
from trading_bot import *
from configuration import *

bot_config = BotConfiguration("./config/bot_config.ini")
bot_info = bot_config.load()

new_bot = TradingBot(bot_info)

new_bot.run()