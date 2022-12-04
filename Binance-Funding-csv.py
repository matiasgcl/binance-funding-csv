# Binance funding rates between given dates, requires requests, time, csv.
# output: csv file
# Binance API info: Data is returned in ascending order. Oldest first, newest last.
# Contact: matiasgcl@protonmail.com - Discord: Matías#1544

# A small script to get funding rates for a given symbol on a given date range
# (it will warn you if the data range is bigger than what Binance API provides
# on a single query (100 results from the initial date, so a bit more than a
# month is the limit)), it outputs a csv file named
# contract-initialFunding-to-finalFundingRegistered.csv
# in which each row contains: symbol, funding time (in readable format), funding rate.

import requests
import time
import csv

aux = requests.get('https://fapi.binance.com/fapi/v1/exchangeInfo').json()
res = [i['symbol'] for i in aux['symbols'] if i['contractType']=='PERPETUAL']
print('List of PERPETUAL contracts')
print(res)
print('Introduce the contract you want the funding rates from: ')
symb = input()
symb = symb.upper()
print('Introduce initial-date for funding in format YYYY-MM-DD hh:mm:ss (24 hour format, UTC time), example: 2022-11-30 14:35:10')
tini = input()
tini = time.mktime(time.strptime(tini, "%Y-%m-%d %H:%M:%S"))
tini *= 1000
tini = int(tini)
print('Introduce end-date for funding in format YYYY-MM-DD hh:mm:ss (24 hour format, UTC time), example: 2022-11-30 14:35:10')
tfin = input()
tfin = time.mktime(time.strptime(tfin, "%Y-%m-%d %H:%M:%S"))
tfin *= 1000
tfin = int(tfin)
aux = requests.get('https://fapi.binance.com/fapi/v1/fundingRate',params={'symbol':symb,'startTime':tini,'endTime':tfin}).json()
supp = aux

# A simple way to extend the data in case the original request reached the limit
# (100 results) I define a supplementary variable, this one contains funding
# rates *starting* on the previous last time + 1s (so it does not repeat),
# I keep doing this until the output (Binance API) gives an empty result
# i.e. when this moving-initial-time is close enough to user-given-final-time
# such that there is no new funding data, or equivalently, the result has
# length zero.
while(len(supp) != 0):
    newinit = aux[len(aux)-1]['fundingTime'] + 1000
    supp = requests.get('https://fapi.binance.com/fapi/v1/fundingRate',params={'symbol':symb,'startTime':newinit,'endTime':tfin}).json()
    aux.extend(supp)

# format  {'symbol': 'BTCUSDT', 'fundingTime': 1666569600009, 'fundingRate': '0.00010000'}
# fundingTime is based on Unix epoch time (ms instead of seconds, beware!)
# fundingRate is in absolute terms (i.e. to get the % should be multiplied by 100),
# this allows to get the funding directly by multiplying position_size*this_number

for i in range(len(aux)):
    # ms to seconds
    aux[i]['fundingTime'] /= 1000.0
    # ':' is not allowed for filenames, so I pick initial and final time for the filename with special format
    if i==0: first = time.strftime('%Y-%m-%d %H.%M', time.gmtime(aux[i]['fundingTime']))
    if i==len(aux)-1: last = time.strftime('%Y-%m-%d %H.%M', time.gmtime(aux[i]['fundingTime']))
    aux[i]['fundingTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(aux[i]['fundingTime']))

filename = 'Funding-'+symb+'-'+first+'-to-'+last+'.csv'

with open(filename, 'w', newline='') as f:
    for i in range(len(aux)):
        if(i==0):
            w = csv.DictWriter(f, aux[i].keys())
            w.writeheader()
        w.writerow(aux[i])
print('Success!\nData saved in '+filename)
print('First funding time registered: '+aux[0]['fundingTime'])
print('Last funding time registered: '+aux[len(aux)-1]['fundingTime'])
print('\nCorrections-commentaries-new ideas : matiasgcl@protonmail.com')
print('\nWas this script useful? A tip (or a thank you if you cant tip) will always be welcome \nEthereum erc20: 0xDc3d1a7566a536CFbcaAeb0CD2a179d78062B4b6')
