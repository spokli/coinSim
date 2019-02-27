'''
Created on 20.08.2017

@author: Marco
'''

from root.nested import Bid
from threading import Thread
import datetime
import collections
import Logger
import time

class Bot:
    
    name = ""
    euroWallet = 0.0
    coinWallet = 0.0
    coinList = {}
    orderedCoinList = {}
    history = []
    ignoredIds = []
    maxBuyPrice = 0  # TODO: set by course values
    api = None
    
    def __init__(self, name, euroWallet, coinWallet, maxBuyPrice, api):
        self.name = name
        self.euroWallet = euroWallet
        self.coinWallet = coinWallet
        self.maxBuyPrice = maxBuyPrice
        self.api = api
    
    def startBuyAndSellThread(self):
        t = Thread(target=self.buyAndSellProcess, args=())
        t.start()
        
    def buyAndSellProcess(self):
        while(True):
            self.tick()
            self.buyProcess()
            self.sellProcess()
            time.sleep(2)
    
    def buyProcess(self):  
        # Read cheapest bid that wasn't bought before
        bid = self.api.getCheapestBid(self.ignoredIds)
        
        if(bid == None):
            Logger.log("Bot " + self.name + ": No bid found", 9)
            return
        
        # check if should buy
        if (self.buyDecision(bid)):
            # buy
            Logger.log("Buying " + str(bid), 4)
            self.buy(bid)
            Logger.log(self, 4)
        else:
            Logger.log("Not buying " + str(bid), 2)
            
            
    def buyDecision(self, bid):
        # Check if affordable.
        Logger.log("Checking buy decision for " + str(bid) + ":", 0)
        
        if (self.euroWallet >= bid.getEuroVolume()):
            # Affordable. Now check if we want to buy
            Logger.log("\t" + "... bid is affordable", 0)
            
            if (bid.price <= self.maxBuyPrice):
                # We want to buy
                Logger.log("\t" + "... price is smaller than defined max price of " + str(self.maxBuyPrice) + ", so buy!", 0)
                return True
            else:
                Logger.log("\t" + "... price is higher than defined max price of " + str(self.maxBuyPrice) + ", so dont buy!", 0)
                return False
                
        else:
            # TODO: maybe it is worth to sell something to buy this one
            return False
    
    def buy(self, bid):
        # Pay in Euro
        self.euroWallet -= bid.getEuroVolume()
        
        # Receive coins
        self.coinWallet += bid.coin
        
        # Add to coinlist
        if (bid.price in self.coinList):
            self.coinList[bid.price] += bid.coin
        else:
            self.coinList[bid.price] = bid.coin
            self.orderedCoinList = collections.OrderedDict(sorted(self.coinList.items()))
        
        # Add to history
        self.history.append(bid)
        
        # Add to ignored Ids
        self.ignoredIds.append(bid.id)
        

    def sellProcess(self):
        # Read most expensive ask that wasn"t sold before
        ask = self.api.getMostExpensiveAsk(self.ignoredIds)
        
        if(ask == None):
            Logger.log("Bot " + self.name + ": No ask found", 9)
            return
        
        toBeSold = self.sellDecision(ask)
        if (not(toBeSold == None)):
            # sell
            Logger.log("Selling to " + str(ask), 4)
            self.sellList(toBeSold, ask)
            self.ignoredIds.append(ask.id)
            
            Logger.log(self, 4)
            
        else:
            Logger.log("Not selling to " + str(ask), 2)
            

    def sellDecision(self, ask):
        Logger.log("Checking sell decision for " + str(ask) + ":", 0)
        
        # Check, if enough coins available to sell
        if(self.coinWallet >= ask.coin):
            # Sellable. Now check if we want to sell
            Logger.log("\t" + "... ask is sellable", 0)
            
            sellableAmount = 0.0
            toBeSold = []
            
            for price, amount in self.orderedCoinList.items():
                if(price < ask.price):
                    sellableAmount += amount
                    toBeSold.append((price, amount))
                    if(sellableAmount >= ask.coin):
                        return toBeSold
            return None
                   
                    
    def sell(self, price, amount):
        if(self.coinList[price] <= amount):
            del self.coinList[price]
        else:
            self.coinList[price] -= amount
        self.orderedCoinList = collections.OrderedDict(sorted(self.coinList.items()))
            
    def sellList(self, toBeSold, ask):
        
        self.euroWallet += ask.price * ask.coin
        
        i = 0 
        restAmountToBeSold = 0 + ask.coin
        while(i < len(toBeSold)):
            price = (toBeSold[i])[0]
            soldAmount = (toBeSold[i])[1]
            self.sell(price, restAmountToBeSold)  # restAmountToBeSold can be higher than the posessed coin amount for this price
            restAmountToBeSold -= soldAmount 
            i += 1

        
    def __str__(self):
        coinListString = ""
        for price, amount in self.orderedCoinList.items():
            coinListString += "\t" + str(price) + "€ \t" + str(amount) + "BTC \n" 
        return "Bot " + self.name + ": Total " + str(self.euroWallet) + "€, " + str(self.coinWallet) + "BTC" + "\n" + coinListString
    def __repr__(self):
        return self.__str__()
   
    def tick(self):
        print(str(datetime.datetime.now()))