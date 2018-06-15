#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 21:31:59 2018

@author: xingyichong
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime

from bs4 import BeautifulSoup as bs
import requests

from pandas_datareader import data as pdr
import fix_yahoo_finance
fix_yahoo_finance.pdr_override()


ToReturn = lambda df: df.iloc[-1]/df.iloc[0] - 1

def DownloadDJIComp():
    '''
    Download the DJI Component symbols from Yahoo Finance
    '''

    YAHOODJIURL = 'https://finance.yahoo.com/quote/%5EDJI/components?p=%5EDJI'
    response = requests.get(YAHOODJIURL)
    soup = bs(response.text, 'lxml')
    
    table = soup.find('table', {'class', 'W(100%) M(0) BdB Bdc($finLightGray)'})
    
    for i in table.findAll('tr')[1:31]:
        item = i.findAll('td')
        yield item[0].text, item[1].text
        



def DownloadDJIPrc(year = 2018):
    '''
    Download the DJI Index Price
    '''
    return pdr.get_data_yahoo('^DJI', str(year)+'-01-01', str(year)+'-12-31').Close



def DownloadCompPrc(tickers, year = 2018):
    '''
    Download the price of every DJI Component as of the specific year
    '''
    if not isinstance(tickers, list):
        tickers = list(tickers)

    return pdr.get_data_yahoo(list(tickers), str(year)+'-01-01', str(year)+'-12-31').Close



def SplitPoint(Sr, SplitCriteria):
    
    '''
    Split the return based on the user input criteria.
    Criterias:
        1. Low: split at the lowest price of the Time Series( The second Param: Ts)
        2. High: split at the highest price
        3. Specific TimeStamp. i.e. 20180201
    '''
    if SplitCriteria in Sr.index:
        return datetime.strptime(SplitCriteria, '%Y%m%d')
    elif  SplitCriteria == 'Low':
        return Sr.idxmin()
    elif SplitCriteria == 'High':
        return Sr.idxmax()
    else:
        raise ValueError ('THe Split Critria must be Low, High or any specific date during the year!')
    

def ReturnSplit(DF, Sr, SplitDay):
        
    DF1 = DF[:SplitDay]
    DF2 = DF[SplitDay:]
    
    Ret1 = ToReturn(DF1)
    Ret2 = ToReturn(DF2)
    
    FinalRet = pd.concat([Ret1,Ret2], axis = 1)
    SplitMonDay = SplitDay.strftime('%B%d')
    
    FinalRet.columns = ['January - ' + SplitMonDay, SplitMonDay + ' - ' + Sr.index[-1].strftime('%B%d')]
    
    return FinalRet



def scatterplot(SplitedReturn, Sr, Splitday, SaveorNo = False):
    
    xmin, ymin = round(SplitedReturn.min(),3)
    xmax, ymax = round(SplitedReturn.max(),3)
    x, y = SplitedReturn.columns
    
    sns.set_style("darkgrid")
    pl = sns.regplot(data=SplitedReturn, x=x, y=y, fit_reg=False, marker="o", color="skyblue", scatter_kws={'s':15})


    for line in range(SplitedReturn.shape[0]):
         pl.text(SplitedReturn[x][line], SplitedReturn[y][line], SplitedReturn.index[line], horizontalalignment='right',
                 size='small', color='black')
    
    bm1 = ToReturn(Sr[:Splitday])
    bm2 = ToReturn(Sr[Splitday:])
    
    pl.plot([bm1, bm1],[ymin, ymax], linewidth = 0.5, color = 'mediumvioletred', linestyle = '--')
    pl.plot([xmin, xmax], [bm2, bm2], linewidth = 0.5, color = 'mediumvioletred', linestyle = '--')
    pl.plot([xmin, xmax], [0, 0], linewidth = 0.5, color = 'blue')
    pl.plot([0, 0],[ymin, ymax],linewidth = 0.5, color = 'blue')
         
    sign = lambda x: '+' if x > 0 else ''
     
    pl.text(xmin, bm2, 'DJI '+ sign(bm2) + "%.2f" % (bm2*100) + '%', color='mediumvioletred', size='small')
    pl.text(bm1, ymin, 'DJI '+ sign(bm1) + "%.2f" % (bm1*100) + '%', color='mediumvioletred', size='small')                 
    
    if SaveorNo:
        figure = pl.get_figure()    
        figure.savefig('djith2017.png', dpi=800)
     
               

def Test(AsofYear, Save):
    
    DJIcompDict = dict(DownloadDJIComp())   # download symbol list
        
    DJI = DownloadDJIPrc(AsofYear)     # Download DJI Price
    DJIComp = DownloadCompPrc(DJIcompDict, AsofYear)   # Download all the components price
    
    SplitDay = SplitPoint(DJI, 'Low')   # Set split point
    ret = ReturnSplit(DJIComp, DJI, SplitDay)   # Return the 2 period returns as a Dataframes with two columns
    
    scatterplot(ret, DJI, SplitDay, Save)   # plot the scatter graph with benchmark movement


if __name__ == '__main__':
    Test(2018, Save = True)
