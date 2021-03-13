#!/usr/bin/python3
#
# See https://sidestory.pandanote.info/xtzjpy_sample.html for details.
#

import httplib2
import io
import sys
import json
import argparse

parser = argparse.ArgumentParser(description='Command line options of xtzjpy.py')
parser.add_argument('-a','--amount', type=str, help='Amount of XTZ.')
parser.add_argument('-i','--amount-file', type=str, help='JSON file to read amount.')

args = parser.parse_args()
params = vars(args)
amount_file = params['amount_file']
amount = params['amount']

if amount_file is not None:
    amount_list = {}
    with open(amount_file) as dbfile:
        t = dbfile.read()
        amount_list = json.loads(t)
        amount = amount_list["amount"]["XTZ"]

r = httplib2.Http()

response, content = r.request('https://api.tzstats.com/markets/tickers', 'GET')

xtzusddata = list(filter(lambda i: i['quote'] == "USD", json.loads(content)))

rvsum = 0
volumesum = 0

for d in xtzusddata:
    rvsum += float(d["last"])*float(d["volume_base"])
    volumesum += float(d["volume_base"])

xtzusdrate = rvsum / volumesum

exchangeapiurl = 'https://api.exchangeratesapi.io/latest?base=USD'

response, content = r.request(exchangeapiurl, 'GET')

usdjpyrate = float(json.loads(content)["rates"]["JPY"])

xtzjpyrate = xtzusdrate*usdjpyrate

print("XTZUSD={0:f},USDJPY={1:f},XTZJPY={2:f}"
      .format(xtzusdrate, usdjpyrate, xtzjpyrate))

if amount is not None:
    tmpam = float(amount)
    print("Estimated amount of mine: {0:f} XTZ, {1:f} USD, {2:f} JPY"
          .format(tmpam, xtzusdrate*tmpam, xtzjpyrate*tmpam))
