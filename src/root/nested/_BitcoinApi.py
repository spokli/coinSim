'''
Created on 20.08.2017

@author: Marco
'''
from root.nested import Bidfrom root.nested import Singleton
import datetime
import requests
import json
from threading import Thread
import time
import Logger

          
def getApi():
    return BitcoinApi.Instance()

@Singleton.Singleton
class BitcoinApi:
    
    ##########################
    # Use offline mode to test
    offline = True
    ##########################
    
    bids = []
    asks = []
    lastUpdateTime = datetime.datetime.min
    querylock = False
    
    def isQueryAllowed(self):
        return (datetime.datetime.now() - self.lastUpdateTime) > datetime.timedelta(seconds=30)       

    def getCheapestBid(self, ignoredIds):

        # Assuming the bids are ordered, return the first one, that is not ignored
        for bid in self.bids:
            if(bid.id not in ignoredIds):
                return bid
            
        return None
    
    def getMostExpensiveAsk(self, ignoredIds):

        # Assuming the asks are ordered, return the first one, that is not ignored
        for ask in self.asks:
            if(ask.id not in ignoredIds):
                return ask
            
        return None
    
    def startApiThread(self):
        t = Thread(target=self.getBidsAndAsks, args=())
        t.start()
    
    def getBidsAndAsks(self):
        while(True):
            if(self.isQueryAllowed() & self.querylock == False):
                self.querylock = True
                
                tmpBids = []
                tmpAsks = []
                
                Logger.log("API: Receiving new orderbook data...", 0)
                
                if(self.offline):
                    # Offline usage
                    with open('orderbook.json') as file:
                        jsonData = json.load(file)
                else:
                    # Online usage
                    r = requests.get("https://bitcoinapi.de/v1/YOUR_API_KEY/orderbook.json")
                    jsonData = r.json()
    
                #-------
                for entry in jsonData['entries']:
                        bid = Bid.Bid()
                        bid.id = entry['id']
                        bid.price = entry['price']
                        bid.coin = entry['amount']
                        bid.date = "?"
                        
                        if (entry['type'] == "bid"):
                            tmpBids.append(bid)
                        elif (entry['type'] == "ask"):
                            tmpAsks.append(bid)
                #-------
                    
                self.bids = tmpBids
                self.asks = tmpAsks
                
                self.lastUpdateTime = datetime.datetime.now()
                self.querylock = False
            
            else:
                Logger.log("API: Bids and asks query failed because locked or too high frequency", 3)
        
            time.sleep(1)

