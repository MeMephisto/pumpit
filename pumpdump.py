#!/usr/bin/env python
from bittrex import bittrex
import sys, signal, json
from pprint import pprint

# Loads settings
with open('settings.json') as data_file:    
    settings = json.load(data_file)

apiKey = settings["apikey"]
apiSecret = settings["secretkey"]
buy = settings["buy"]
sell = settings["sell"]


# Get these from https://bittrex.com/Account/ManageApiKey
api = bittrex(apiKey, apiSecret)

# Gets your BTC balance before the pump to save time
btcBalance = api.getbalance("BTC")['Available']

# Set to True to enable limit trading
allow_orders = True
	
# Sets the amount to use in the pump
print 'You have {} BTC available.'.format(btcBalance)
pumpAmount = raw_input("Amount to use in pump: ")
print 'Using {} BTC in the pump'.format(pumpAmount)

pumpCoin = raw_input("Coin: ")
coinPrice = api.getticker("BTC-" + pumpCoin)
askPrice = coinPrice['Ask']

# Change accordingly
customBuy = askPrice + (buy * askPrice)
customSell = askPrice + (sell * askPrice)


print 'Current ask price for {} is {} BTC.'.format(pumpCoin, askPrice)

# Calculates the number of pumpCoins to buy, taking into consideration Bittrex's 0.25% fee
numCoins = (pumpAmount - (pumpAmount*0.00251)) / customBuy

buyPrice = customBuy * numCoins
sellPrice = customSell * numCoins
profit = sellPrice - buyPrice

print '\n[+] Buying {} {} coins at {} BTC each for a total of {} BTC'.format(numCoins,
        pumpCoin, customBuy, buyPrice)

if allow_orders:
    print api.buylimit('BTC-' + pumpCoin, numCoins, customBuy)
else:
    print "[!] allow_orders = False in script... change to make orders..."

print '[+] Placing sell order at {} ...'.format(customSell)

if allow_orders:
    print api.selllimit('BTC-' + pumpCoin, numCoins, customSell)
else:
    print "[!] allow_orders = False in script... change to make orders..."

print '[+] Profit if sell order gets bought: {} BTC'.format(profit)
