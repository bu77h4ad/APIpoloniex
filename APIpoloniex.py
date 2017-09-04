import requests
from urllib.parse import urlencode 

import json 
from hmac import new 
from hashlib import sha512 
import logging

# 3rd party
import sys
import time

class APIpoloniex(object):	
	def APIerror(self,command, info):
		print( "\n"+time.strftime("[%H:%M:%S]")+" Error while executing the command: " + "\"" +command + "\"")
		print(time.strftime("[%H:%M:%S]"),info)
		return

	def __init__(self,APIKey,Secret,timeout_sec=3.0):
		self.APIKey=APIKey
		self.Secret=Secret
		self.timeout_sec= timeout_sec
		# set time labels
		self.MINUTE, self.HOUR, self.DAY = 60, 60 * 60, 60 * 60 * 24
		self.WEEK, self.MONTH = self.DAY * 7, self.DAY * 30
		self.YEAR = self.DAY * 365
		return

	#Функция для публичных команд
	def CommandPublic (self, command, args={}, timeout_sec=False):
		if timeout_sec == False : timeout_sec= self.timeout_sec
		url = 'https://poloniex.com/public?command=' + command
		if args.get("currencyPair"): url= url +"&currencyPair=" + args['currencyPair']			
		if args.get("period"): url= url +"&period=" + args['period']	
		if args.get("start"): url= url +"&start=" + args['start']	
		if args.get("end"): url= url +"&end=" + args['end']	
		try:
			html = requests.get(url,timeout=(timeout_sec,timeout_sec))
		except:
			self.APIerror(command,sys.exc_info()[1])
			return -1
		else:				
			return html.json()

	#Функция для приватных команд
	def CommandPrivate(self,command="",args={},timeout_sec=False): #
		if timeout_sec == False : timeout_sec= self.timeout_sec
		args['command'] = command
		args['nonce'] =  int(time.time()*1000000)		
		url = "https://poloniex.com/tradingApi"
		sign = new(
                self.Secret.encode('utf-8'),
                urlencode(args).encode('utf-8'),
                sha512).hexdigest()
		headers = {
		'Key' : self.APIKey,
		'Sign' :sign,
		}    
		try:
			html = requests.post(url, data=args, headers=headers,timeout=(timeout_sec, timeout_sec))
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

#returnBalances Показывает баланс
	def returnBalances(self):		
		return self.CommandPrivate('returnBalances')

#returnTradeHistory показывает историю моих сделок	
	def returnTradeHistory(self,currencyPair='all', start=False, end=False):
		if start == 0 : start = time.time()- self.DAY
		if end == 0 : end = time.time()
		args = {'currencyPair':currencyPair,
				'start'	: start,
				'end'	: end
				}		
		return self.CommandPrivate('returnTradeHistory',args)

#returnTicker текущее значения на бирже
	def returnTicker(self):
		return self.CommandPublic('returnTicker')

#returnChartData 
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


"""a =APIpoloniex('TJB1WD64-PCB1C4SZ-XMZ67F35-JW8WX5JG',
	'd6419326159dca9ac230096c61f3bb1e4fe725f4c7a71123377693485308206b37735f98d3870fc12e25f5cdb1cd523d6e3837b3cf33aa6c1754157a6170f94c')
print ( a.returnOpenOrders('BTC_SC'))
#print(a.returnTicker())
#print(a.returnChartData("BTC_SC",period=86400) )
#print (a.returnTradeHistory(start= time.time() - 3600*24*1) )"""
