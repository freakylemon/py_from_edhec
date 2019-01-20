# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 20:35:53 2018

@author: freakylemon
"""
import datetime as dt
import pandas as pd
import numpy as np
from math import sqrt
ddd = pd.read_pickle('./MM_stock_data_NEW.pkl')
ddd.columns
'''daily trading volume'''
dtrvo = ddd.Volume.mean()

'''average daily value of the inverse of the price'''
avInvPrice = (1/ ddd['Close']).mean()
list1 = []
for char in avInvPrice:
    list1.append(char)

'''Daily Volatility-- I made it in average'''


#这个列表 里面有所有的ticker
ttic = []
for char in ddd['Open'][:0]:
    ttic.append(char)

pp = ddd[ddd.index.month == 5]['Adj Close'].std()

# 
pp = {}
for i in range (1,13):
    pp[i] = ddd[ddd.index.month == i]['Adj Close'].std()

#试一下
#pp[4]['AY']

avvList = []
for char in ttic:
    avv = 0
    for i in range(1, 13):
        avv += (pp[i][char])
    avvList.append(avv/12)    

#这里是一种方法 存储-- ticker-volatility pair
avvDic = {}
i = 0
for char in ttic:
    if i < 30:
        avvDic[char] = avvList[i] 
        i += 1
#这是另一种方法-- 存储-- ticker-volatility pair
ppp = pd.DataFrame([avvList], columns = [char for char in ttic], index = ['Volatility']).T
#我碰到了问题-- 为什么 dataframe 是列-- 不能是行-- 
ppp['dailyTradingVolume'] = dtrvo
ppp['avDailyValue'] = list1

'''Roll's Effective Spread??'''
