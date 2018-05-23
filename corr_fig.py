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

        }

def eq(Year, bm_list, col = 'Close'):
    return pdr.get_data_yahoo(bm_list, 
                              start = str(Year) + "-01-01", 
                              end = str(Year) + "-12-31")[col]

def year_return(xd, rtn_type = 'norm'):   # norm return or log return
    cng = xd[-1] / xd[0] - 1
    if rtn_type == 'log':
        return np.log(cng + 1)
    return cng

def _corrplt_3bm(year, daily_rtn, annual_rtn):

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


def corrplot(sym_list, year_test):

    symbol_list = [BM_DICT[name] for name in sym_list]
    BM_raw = eq(year_test, symbol_list)
    BM_raw = BM_raw.rename(columns = dict(zip(symbol_list,sym_list)))
    
    print(BM_raw.shape[0])
    
    BM_annual_rtn = BM_raw.pct_change(BM_raw.shape[0]-1).iloc[-1]
    BM_daily_rtn = BM_raw.pct_change(1)
    
    _corrplt_3bm(year_test, BM_daily_rtn, BM_annual_rtn)


if __name__ == '__main__':
    corr_list1 = ['S&P500', 'USD', 'MSCI EM']
    corrplot(corr_list1, 2017)
    corrplot(corr_list1, 2008)

