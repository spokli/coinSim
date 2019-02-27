"""
Created on 20.08.2017

@author: Marco
"""
from root.nested import Bot
from root.nested import _BitcoinApi

def main():
    api = _BitcoinApi.getApi()
    api.startApiThread()
    bot1 = Bot.Bot("A", 10000, 0, 3510, api)
    bot1.startBuyAndSellThread()


main()