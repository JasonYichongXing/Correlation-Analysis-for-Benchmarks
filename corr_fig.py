#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 22 23:45:35 2018

@author: xingyichong
"""
import numpy as np
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
from pandas.plotting import scatter_matrix
import fix_yahoo_finance

fix_yahoo_finance.pdr_override()


BM_DICT = {
        'S&P500': '^GSPC',
        'USD': 'DX-Y.NYB',
        'US10YR': '^TNX',
        'MSCI EM': 'EEM',
 # dictionary for symbol mapping table, to be added...
        }

def eq(Year_start, Year_end, bm_list, col = 'Close'):
    '''
    Function to download time series data from yahoo finance (with fix patch May' 2018)
    '''
    return pdr.get_data_yahoo(bm_list, 
                              start = str(Year_start) + "-01-01", 
                              end = str(Year_end) + "-12-31")[col]



def year_return(xd, rtn_type = 'norm'):   # norm return or log return
    cng = xd[-1] / xd[0] - 1
    if rtn_type == 'log':
        return np.log(cng + 1)
    return cng

def _corrplt_3bm(year, daily_rtn, annual_rtn):
    '''
    private function to generate the correlation scatter graph for two time series.
    Time frame is one calendar year.
    Mainly utilize Dataframe.corr().
    '''
    s = scatter_matrix(daily_rtn, figsize = (10,10), alpha = 0.4, diagonal='kde')

    s[0,0].annotate('YTD = %.2f' %annual_rtn[0], (0,0), ha='center')
    s[1,1].annotate('YTD = %.2f' %annual_rtn[1], (0,0), ha='center')
    s[2,2].annotate('YTD = %.2f' %annual_rtn[2], (0,0), ha='center')
    
    corr_mat = daily_rtn.corr().as_matrix()
    
    s[1,0].annotate('corr = %.3f' %corr_mat[1,0], xy=(0,-0.02), ha='center')
    s[2,0].annotate('corr = %.3f' %corr_mat[2,0], xy=(0,-0.012), ha='center')
    s[2,1].annotate('corr = %.3f' %corr_mat[2,1], xy=(0,-0.012), ha='center')
    
    for i in s.reshape(-1):
        i.set_yticks(())
        i.set_xticks(())
        i.xaxis.label.set_rotation(0)
        i.yaxis.label.set_rotation(0)
        i.get_yaxis().set_label_coords(-0.25,0.5)
    
    plt.suptitle('\nIndex Correlation Scatter Graph\n' + str(year), fontsize=20)
    
    plt.savefig('corrfig'+ str(year), dpi=900)


def corrplot(sym_list, year_start, year_end):
    '''
    Main function to generate corr scatter graph.
    Input:
        Symbol name list, start year and end year
    '''
    symbol_list = [BM_DICT[name] for name in sym_list]
    BM_raw = eq(year_start, year_end, symbol_list)
    BM_raw = BM_raw.rename(columns = dict(zip(symbol_list,sym_list)))
        
    BM_annual_rtn = BM_raw.pct_change(BM_raw.shape[0]-1).iloc[-1]
    BM_daily_rtn = BM_raw.pct_change(1)
    
    _corrplt_3bm(year_start, BM_daily_rtn, BM_annual_rtn)


def rollingcorr(window, raw2d):
    '''
    Generate the rolling correlation with user input moving time window.
    Mainly utilize Dataframe.rolling(Days).corr() function.
    Input:
        time window, time series of 2 indexs.
    '''
    if window >= raw2d.shape[0]:
        raise 'Time Frame Exceed '
    
    index_name = raw2d.columns.values[0] 
    rawcorr = raw2d.rolling(window).corr()
    corr_pair = rawcorr[index_name].iloc[1::2]
    corr_pair.index = [_time[0] for _time in corr_pair.index]
    
    return corr_pair


if __name__ == '__main__':
    corr_list1 = ['S&P500', 'USD', 'MSCI EM']
    symbol_list = [BM_DICT[name] for name in corr_list1]
    
    #test1 for plotting scatter matrix as of 2008 & 2017
    corrplot(corr_list1, 2017, 2017)
    corrplot(corr_list1, 2008, 2008)
    
    #test2 for plot 3m moving corr during 2000 - 2018
    raw = eq(2004, 2018, symbol_list)
    raw_daily_rtn = raw.pct_change(1)
    raw_daily_rtn = raw_daily_rtn.rename(columns = dict(zip(symbol_list,corr_list1)))
    rtest1 = raw_daily_rtn[['MSCI EM','S&P500']].copy()
    
    window = 90
    corrforplot = rollingcorr(window, rtest1)
    plt.plot(corrforplot)
    corr_mean = np.mean(corrforplot)
    count_timestamp = corrforplot.shape[0]
    
    line1, = plt.plot(corrforplot.index, [corr_mean]*count_timestamp, label= 'Corr Meam', linestyle='--')
    plt.title('%sm rolling corr between MSCI EM and S&P500' % (window // 30), fontsize=11)
    plt.savefig('rollingcorr', dpi=900)