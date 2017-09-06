#In English
#  The APIpoloniex class works with the API https://poloniex.com/ 
#
# This class has an error handler for poloniex requests, thanks to this
# Your trading terminal will not hang for a long time.
# 
# If the query data, poloniex.com does not respond more timeOutSec seconds,
# then the function returns -1 and an error message is displayed (APIerror)
# 
# The script is written for yourself, for trading on the stock exchange. Distributed without a license

#Для Русских
#  Класс APIpoloniex работает с API https://poloniex.com/ 
#
# В данный клас встроен обработчик ошибок на запросы к poloniex, благодаря этому
# Ваш торговый терминал не будет зависать на длительное время.
#  
# Если на запрос данных, poloniex.com не отвечает больше timeOutSec секунд, 
# то функция возвращает -1 и выводится сообщение об ошибке (APIerror)
# 
# Скрипт написан для себя, для торговли на бирже. Распростроняется без лицензии

#For Example 
#
# from APIpoloniex import *
# polo = APIpoloniex('api_key', 'api_secret',1.0)
# print (polo.returnBalances())

#Donate
#
# BTC fb0a34933ca0781f5e9917a52ea86d72cbb1c05b4ccfff56f9c78bdce5f8a573
# LTC LRsm54XYJxG7NJCuAntK98odJoXhwp1GBK
# ETH 0x8750793385349e2edd63e87d5c523b3b2c972b82


import requests
from urllib.parse import urlencode 
import json 
from hmac import new 
from hashlib import sha512 
import sys
import time

class APIpoloniex(object):	
	"""
	key = str api key supplied by Poloniex
	secret = str secret hash supplied by Poloniex
	timeout = int time in sec to wait for an api response
	"""       
	def __init__(self,APIKey,secret,timeOutSec=3.0):
		self.APIKey=APIKey
		self.secret=secret
		self.timeOutSec= timeOutSec
		# set time labels
		self.MINUTE, self.HOUR, self.DAY = 60, 60 * 60, 60 * 60 * 24
		self.WEEK, self.MONTH = self.DAY * 7, self.DAY * 30
		self.YEAR = self.DAY * 365
		return

#APIerror Вывод ошибок	
	def APIerror(self,command, info):
		""" Exception for handling poloniex api errors """
		print( "\n"+time.strftime("[%H:%M:%S]")+" Error while executing the command: " + "\"" +command + "\"")
		print(time.strftime("[%H:%M:%S]"),info)
		return

#CommandPublic для публичных команд
	def CommandPublic (self, command, args={}, timeOutSec=False):
		"""  """
		if timeOutSec == False : timeOutSec= self.timeOutSec
		url = 'https://poloniex.com/public?command=' + command
		if args.get("currencyPair"): url= url +"&currencyPair=" + args['currencyPair'].upper()			
		if args.get("period"): url= url +"&period=" + args['period']	
		if args.get("start"): url= url +"&start=" + args['start']	
		if args.get("end"): url= url +"&end=" + args['end']	
		try:
			html = requests.get(url,timeout=(timeOutSec,timeOutSec))
		except:
			self.APIerror(command,sys.exc_info()[1])
			return -1
		else:							
			return html.json()

#CommandPrivate для приватных команд		
	def CommandPrivate(self,command="",args={},timeOutSec=False):
		"""  """
		if timeOutSec == False : timeOutSec= self.timeOutSec
		args['command'] = command
		args['nonce'] =  int(time.time()*1000000)			
		url = "https://poloniex.com/tradingApi"
		sign = new(
                self.secret.encode('utf-8'),
                urlencode(args).encode('utf-8'),
                sha512).hexdigest()
		headers = {
		'Key' : self.APIKey,
		'Sign' :sign,
		}    
		try:
			html = requests.post(url, data=args, headers=headers,timeout=(timeOutSec, timeOutSec))
		except:
			self.APIerror(command,sys.exc_info()[1])
			return -1	
		else:				 
			return  html.json()

# --PUBLIC COMMANDS-------------------------------------------------------

	def returnTicker(self,timeOutSec = False):	
		""" Returns the ticker for all markets. 
		Sample output:
		{"BTC_LTC":{"last":"0.0251","lowestAsk":"0.02589999","highestBid":"0.0251","percentChange":"0.02390438",
		"baseVolume":"6.16485315","quoteVolume":"245.82513926"},"BTC_NXT":{"last":"0.00005730","lowestAsk":"0.00005710",
		"highestBid":"0.00004903","percentChange":"0.16701570","baseVolume":"0.45347489","quoteVolume":"9094"}, ... } """	
		return self.CommandPublic('returnTicker', timeOutSec = timeOutSec)

	def return24hVolume(self,timeOutSec = False):
		""" Returns the 24-hour volume for all markets, plus totals for primary currencies. 
		Sample output:
		{"BTC_LTC":{"BTC":"2.23248854","LTC":"87.10381314"},"BTC_NXT":{"BTC":"0.981616","NXT":"14145"}, ... 
		"totalBTC":"81.89657704","totalLTC":"78.52083806"} """				
		return self.CommandPublic('return24hVolume', timeOutSec = timeOutSec)

	def returnOrderBook(self,currencyPair='all', timeOutSec=False):
		""" Returns the order book for a given market, as well as a sequence number for use with the Push API 
		and an indicator specifying whether the market is frozen. You may set currencyPair to "all" 
		to get the order books of all markets. 
		Sample output:
		{"asks":[[0.00007600,1164],[0.00007620,1300], ... ], "bids":[[0.00006901,200],[0.00006900,408], ... ], "isFrozen": 0, "seq": 18849} """
		args = { 
			'currencyPair' : currencyPair
		}
		return self.CommandPublic('returnOrderBook',args = args , timeOutSec = timeOutSec)

	def returnChartData(self, currencyPair, period=False, start=False, end=False, timeOutSec=False):
		""" Returns candlestick chart data. Required GET parameters are "currencyPair", "period" (candlestick period in seconds; 
		valid values are 300, 900, 1800, 7200, 14400, and 86400), "start", and "end". "Start" and "end" are given in UNIX timestamp
		format and used to specify the date range for the data returned. 
		Sample output:
		[{"date":1405699200,"high":0.0045388,"low":0.00403001,"open":0.00404545,"close":0.00427592,"volume":44.11655644,
		"quoteVolume":10259.29079097,"weightedAverage":0.00430015}, ...] """
		if period not in [300, 900, 1800, 7200, 14400, 86400]:
			print ("%s invalid candle period" % str(period))
		if not start:
			start = time.time() - self.DAY
		if not end:
			end = time.time()
		agrs =  {
			'currencyPair': str(currencyPair).upper(),
			'period': str(period),
			'start': str(start),
			'end': str(end)
                }
		return self.CommandPublic('returnChartData', args=agrs, timeOutSec=timeOutSec )

 # --PRIVATE COMMANDS------------------------------------------------------	

	def returnBalances(self, timeOutSec = False):		
		""" Returns all of your available balances. 
		Sample output: 
		{"BTC":"0.59098578","LTC":"3.31117268", ... } """
		return self.CommandPrivate('returnBalances', timeOutSec = timeOutSec)

	def returnCompleteBalances(self, account='all', timeOutSec = False):
		""" Returns all of your balances, including available balance, balance
        on orders, and the estimated BTC value of your balance. By default,
        this call is limited to your exchange account; set the "account"
        parameter to "all" to include your margin and lending accounts. 
        Sample output:
        {"LTC":{"available":"5.015","onOrders":"1.0025","btcValue":"0.078"},"NXT:{...} ... }"""
		args = { 'account' : account }
		return self.CommandPrivate('returnCompleteBalances', args = args, timeOutSec = timeOutSec)

	def returnDepositAddresses(self, timeOutSec = False):
		""" Returns all of your deposit addresses. Sample output: {"BTC":"19YqztHmspv2egyD6jQM3yn81x5t5krVdJ","LTC """
		return self.CommandPrivate('returnDepositAddresses', timeOutSec = timeOutSec)

	def returnTradeHistory(self,currencyPair='all', start=False, end=False, timeOutSec = False):
		""" Returns your trade history for a given market, specified by the
        "currencyPair" parameter. You may specify "all" as the currencyPair to
        receive your trade history for all markets. You may optionally specify
        a range via "start" and/or "end" POST parameters, given in UNIX
        timestamp format; if you do not specify a range, it will be limited to one day. 
        Sample output:
		{"BTC_MAID": [ { "globalTradeID": 29251512, "tradeID": "1385888", "date": "2016-05-03 01:29:55", "rate": "0.00014243",
		"amount": "353.74692925", "total": "0.05038417", "fee": "0.00200000", "orderNumber": "12603322113", "type": "buy", 
		"category": "settlement" }, { "globalTradeID": 29251511, "tradeID": "1385887", "date": "2016-05-03 01:29:55", 
		"rate": "0.00014111", "amount": "311.24262497", "total": "0.04391944", "fee": "0.00200000", "orderNumber": "12603319116", 
		"type": "sell", "category": "marginTrade" }, ... ],"BTC_LTC":[ ... ] ... }"""
		if start == False : start = time.time() - self.DAY
		if end == False : end = time.time()
		args = {'currencyPair':currencyPair,
				'start'	: start,
				'end'	: end
				}		
		return self.CommandPrivate('returnTradeHistory', args=args, timeOutSec = timeOutSec)

	def buy(self, currencyPair, rate, amount, timeOutSec = False):
		""" Places a limit buy order in a given market. Required parameters are
        "currencyPair", "rate", and "amount". You may optionally set "orderType"
        to "fillOrKill", "immediateOrCancel" or "postOnly". A fill-or-kill order
        will either fill in its entirety or be completely aborted. An
        immediate-or-cancel order can be partially or completely filled, but
        any portion of the order that cannot be filled immediately will be
        canceled rather than left on the order book. A post-only order will
        only be placed if no portion of it fills immediately; this guarantees
        you will never pay the taker fee on any part of the order that fills.
        If successful, the method will return the order number.
        Sample output:
		{"orderNumber":31226040,"resultingTrades":[{"amount":"338.8732","date":"2014-10-18 23:03:21","rate":"0.00000173",
		"total":"0.00058625","tradeID":"16164","type":"buy"}]}"""
		args = {
		'currencyPair': str(currencyPair),
		'rate': str(rate),
		'amount': str(amount),
        }
		return self.CommandPrivate('buy',args=args,timeOutSec = timeOutSec)

	def sell(self, currencyPair, rate, amount, timeOutSec = False):
		""" Places a sell order in a given market. Parameters and output are
        the same as for the buy method. """
		args = {
		'currencyPair': str(currencyPair),
		'rate': str(rate),
		'amount': str(amount),
        }
		return self.CommandPrivate('sell',args=args, timeOutSec = timeOutSec)

	def cancelOrder(self, orderNumber, timeOutSec = False ):	
		""" Cancels an order you have placed in a given market. Required
        parameter is "orderNumber". If successful, the method will return:
        {"success":1} """
		args= { 'orderNumber': orderNumber }
		return 	self.CommandPrivate('cancelOrder',args=args, timeOutSec = timeOutSec)

	def returnOpenOrders(self,currencyPair='all',timeOutSec = False):
		""" Returns your open orders for a given market, specified by the
		"currencyPair" parameter, e.g. "BTC_XCP". Set "currencyPair" to
		"all" to return open orders for all markets.
		Sample output for single market:
		[{"orderNumber":"120466","type":"sell","rate":"0.025","amount":"100","total":"2.5"},
		{"orderNumber":"120467","type":"sell","rate":"0.04","amount":"100","total":"4"}, ... ] """
		args = { 'currencyPair': currencyPair }
		return self.CommandPrivate('returnOpenOrders',args=args,timeOutSec = timeOutSec)
