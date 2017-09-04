#In English
#  The APIpoloniex class works with the API https://poloniex.com/ #
#
# This class has an error handler for poloniex requests, thanks to this
# Your trading terminal will not hang for a long time.
# 
# If the query data, poloniex.com does not respond more timeOutSec seconds,
# then the function returns -1 and an error message is displayed (APIerror)
# 
# The script is written for yourself, for trading on the stock exchange. Distributed without a license

#Для Русских
#  Класс APIpoloniex работает с API https://poloniex.com/ #
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
#
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
		print( "\n"+time.strftime("[%H:%M:%S]")+" Error while executing the command: " + "\"" +command + "\"")
		print(time.strftime("[%H:%M:%S]"),info)
		return

#CommandPublic для публичных команд
	def CommandPublic (self, command, args={}, timeOutSec=False):
		if timeOutSec == False : timeOutSec= self.timeOutSec
		url = 'https://poloniex.com/public?command=' + command
		if args.get("currencyPair"): url= url +"&currencyPair=" + args['currencyPair']			
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
	def CommandPrivate(self,command="",args={},timeOutSec=False): #
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

### PUBLIC COMMANDS-----------

#returnTicker текущее значения на бирже
	def returnTicker(self,timeOutSec = False):		
		return self.CommandPublic('returnTicker', timeOutSec = timeOutSec)

#return24hVolume возвращает значения за 24 часа
	def return24hVolume(self,timeOutSec = False):				
		return self.CommandPublic('return24hVolume', timeOutSec = timeOutSec)

#returnOrderBook возвращает стакан цен
	def returnOrderBook(self,currencyPair='all', timeOutSec=False):
		args = { 
			'currencyPair' : currencyPair
		}
		return self.CommandPublic('returnOrderBook',args = args , timeOutSec = timeOutSec)

#returnChartData возвращает историю баров
	def returnChartData(self, currencyPair, period=False, start=False, end=False, timeOutSec=False):

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

### PRIVATE COMMANDS-----------		
# Returns all of your available balances. Sample output: {"BTC":"0.59098578","LTC":"3.31117268", ... }
	def returnBalances(self, timeOutSec = False):		
		return self.CommandPrivate('returnBalances', timeOutSec = timeOutSec)

# Returns all of your balances, including available balance, balance on orders, and the estimated BTC value of your balance.
	def returnCompleteBalances(self, account='all', timeOutSec = False):
		args = { 'account' : account }
		return self.CommandPrivate('returnCompleteBalances', args = args, timeOutSec = timeOutSec)

# Returns all of your deposit addresses. Sample output: {"BTC":"19YqztHmspv2egyD6jQM3yn81x5t5krVdJ","LTC
	def returnDepositAddresses(self, timeOutSec = False):
		return self.CommandPrivate('returnDepositAddresses', timeOutSec = timeOutSec)

# Returns your trade history for a given market, specified by the "currencyPair" POST parameter.
# You may specify "all" as the currencyPair to receive your trade history for all markets.
# You may optionally specify a range via "start" and/or "end" POST parameters, given in UNIX timestamp format;
# if you do not specify a range, it will be limited to one day. 
	def returnTradeHistory(self,currencyPair='all', start=False, end=False, timeOutSec = False):
		if start == False : start = time.time()- self.DAY
		if end == False : end = time.time()
		args = {'currencyPair':currencyPair,
				'start'	: start,
				'end'	: end
				}		
		return self.CommandPrivate('returnTradeHistory', args=args, timeOutSec = timeOutSec)

#BUY Places a limit buy order in a given market. Required POST parameters are "currencyPair", "rate", and "amount".
# If successful, the method will return the order number
	def buy(self, currencyPair, rate, amount, timeOutSec = False):
		args = {
		'currencyPair': str(currencyPair),
		'rate': str(rate),
		'amount': str(amount),
        }
		return self.CommandPrivate('buy',args=args,timeOutSec = timeOutSec)

#SELL Places a sell order in a given market. Parameters and output are the same as for the buy method.
	def sell(self, currencyPair, rate, amount, timeOutSec = False):
		args = {
		'currencyPair': str(currencyPair),
		'rate': str(rate),
		'amount': str(amount),
        }
		return self.CommandPrivate('sell',args=args, timeOutSec = timeOutSec)

# Cancels an order you have placed in a given market. 
# Required POST parameter is "orderNumber". 
# If successful, the method will return: {"success":1}
	def cancelOrder(self, orderNumber, timeOutSec = False ):	
		args= { 'orderNumber': orderNumber }
		return 	self.CommandPrivate('cancelOrder',args=args, timeOutSec = timeOutSec)

# Returns your open orders for a given market, specified by the "currencyPair" POST parameter, e.g. "BTC_XCP".
# Set "currencyPair" to "all" to return open orders for all markets
	def returnOpenOrders(self,currencyPair='all',timeOutSec = False):
		args = { 'currencyPair': currencyPair }
		return self.CommandPrivate('returnOpenOrders',args=args,timeOutSec = timeOutSec)
