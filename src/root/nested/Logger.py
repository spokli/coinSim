'''
Created on 20.08.2017

@author: Marco
'''

# level = 'All' # = 0
# level = 'Transaction' # = 2
level = 'Successful Transaction' # = 4
# level = 'Error' # = 9


def log(message, type):
    if(printable(type)):
        print(message)
    
def printable(type):
    if(level == 'All'):
        return True
    elif(level == 'Transaction' and type >= 2):
        return True
    elif(level == 'Successful Transaction' and type >= 4):
        return True
    elif(level == 'Error' and type >= 9):
        return True
    else:
        return False