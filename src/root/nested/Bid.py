'''
Created on 20.08.2017

@author: Marco
'''
class Bid:
    id = ""
    date = ""
    price = 0.0
    coin = 0.0
    
    def getEuroVolume(self):
        return self.price * self.coin
    
    def __str__(self):
        return "" + str(self.coin) + " coins for " + str(self.price) + "€ per BTC. Total: " + str(self.getEuroVolume()) + "€ (" + self.id + ", " + self.date + ")"
    
    def __repr__(self):
        return self.__str__()
        