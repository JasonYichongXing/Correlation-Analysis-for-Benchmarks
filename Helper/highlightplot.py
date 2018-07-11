#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 23:18:24 2018

@author: xingyichong
"""
# ref: https://python-graph-gallery.com/125-small-multiples-for-line-chart/

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def highlightplot(Data, highlightcolname,
                  highlightcolor='red', title='TEST HIGHLIGHT',
                  xlabel='Xlabel', ylabel='Ylabel'):

    if not isinstance(Data, pd.DataFrame):
        Data = pd.DataFrame(Data)

    plt.plot(Data, color='grey', alpha=0.3)

    # Replot highlight col
    plt.plot(Data[highlightcolname], color=highlightcolor, linewidth=3, alpha=0.9)

    plt.title(title, color=highlightcolor)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)


if __name__ == '__main__':

    test = pd.DataFrame(np.random.rand(10,6), columns=['a', 'b', 'c', 'd', 'e', 'f'])
    highlightplot(test, 'e', 'green', 'RandomTest')
