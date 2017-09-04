# APIpoloniex
Script for working in API poloniex
```python
from APIpoloniex import *
polo = APIpoloniex(APIKey,Secret,[timeout_sec])
print (polo.returnBalances())
```
---
in English

Written on the basis of https://github.com/s4w3d0ff/python-poloniex

The main differences from other poloniex scripts.  
  1. The program does not freeze. if the answer is not received then the polonix, the function returns -1. Timeout default 3 seconds

---
по Русскии 

Написан на основе https://github.com/s4w3d0ff/python-poloniex

Самые главные отличия от других скриптов API poloniex.
  1. Программа не зависает. Если ответ от полоникса не получен в течении (таймаута) , то функция возвращает -1. таймаут по умолчанию 3 сек.
