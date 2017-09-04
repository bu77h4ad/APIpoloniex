#In English
# # # The APIpoloniex class works with the API https://poloniex.com/ #
#
# This class has an error handler for poloniex requests, thanks to this
# Your trading terminal will not hang for a long time.
# #
# If the query data, poloniex.com does not respond more timeOutSec seconds,
# then the function returns -1 and an error message is displayed (APIerror)
# #
# The script is written for yourself, for trading on the stock exchange. Distributed without a license
#
#Для Русских
# #			# Класс APIpoloniex работает с API https://poloniex.com/ #
#
# В данный клас встроен обработчик ошибок на запросы к poloniex, благодаря этому
# Ваш торговый терминал не будет зависать на длительное время.
# # 
# Если на запрос данных, poloniex.com не отвечает больше timeOutSec секунд, 
# то функция возвращает -1 и выводится сообщение об ошибке (APIerror)
# #
# Скрипт написан для себя, для торговли на бирже. Распростроняется без лицензии
#
# #			# For Example #
#
# from APIpoloniex import *
# polo = APIpoloniex('api_key', 'api_secret',1.0)
# print (polo.returnBalances())
# #


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
#BUY функция
	def buy(self, currencyPair, rate, amount):
		args = {
		'currencyPair': str(currencyPair),
		'rate': str(rate),
		'amount': str(amount),
        }
		return self.CommandPrivate('buy',args)
#SELL Функция
	def sell(self, currencyPair, rate, amount):
		args = {
		'currencyPair': str(currencyPair),
		'rate': str(rate),
		'amount': str(amount),
        }
		return self.CommandPrivate('sell',args)

#returnOpenOrders Возвращает Отррытые ордера
	def returnOpenOrders(self,currencyPair='all'):
		args = { 'currencyPair': currencyPair }
		return self.CommandPrivate('returnOpenOrders',args)

#returnBalances Возвращает баланс
	def returnBalances(self):		
		return self.CommandPrivate('returnBalances')

#returnTradeHistory возвращает историю моих сделок	
	def returnTradeHistory(self,currencyPair='all', start=False, end=False):
		if start == False : start = time.time()- self.DAY
		if end == False : end = time.time()
		args = {'currencyPair':currencyPair,
				'start'	: start,
				'end'	: end
				}		
		return self.CommandPrivate('returnTradeHistory',args)

#returnTicker текущее значения на бирже
	def returnTicker(self):
		return self.CommandPublic('returnTicker')

#returnChartData возвращает историю баров
	def returnChartData(self, currencyPair, period=False, start=False, end=False):

		if period not in [300, 900, 1800, 7200, 14400, 86400]:
			print ("%s invalid candle period" % str(period))
		if not start:
			start = time.time() - self.DAY
		if not end:
			end = time.time()
		return self.CommandPublic('returnChartData', {
			'currencyPair': str(currencyPair).upper(),
			'period': str(period),
			'start': str(start),
			'end': str(end)
        })
