# APIpoloniex
Script for working in API poloniex
```python
from APIpoloniex import *
polo = APIpoloniex('APIKey', 'Secret', 3.0)
print (polo.returnBalances()['BTC_LTC'])
```

>in English

The main differences from other poloniex scripts.  
  - The program does not freeze. if the answer is not received then the polonix, the function returns -1. Timeout default 3 seconds


>по Русскии 

Написан на основе https://github.com/s4w3d0ff/python-poloniex

Самые главные отличия от других скриптов API poloniex.
  - Программа не зависает. Если ответ от полоникса не получен в течении (таймаута) , то функция возвращает -1. таймаут по умолчанию 3 сек.

>Donate
- BTC fb0a34933ca0781f5e9917a52ea86d72cbb1c05b4ccfff56f9c78bdce5f8a573
- LTC LRsm54XYJxG7NJCuAntK98odJoXhwp1GBK
- ETH 0x8750793385349e2edd63e87d5c523b3b2c972b82
