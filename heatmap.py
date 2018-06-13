#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 23:55:14 2018

@author: xingyichong
"""

def heatmap(matrix):
    
    import numpy as np
    import seaborn as sns

    dropSelf = np.zeros_like(matrix)
    dropSelf[np.triu_indices_from(dropSelf)] = True     
    colormap = sns.diverging_palette(220, 10, as_cmap=True)
    
    sns.heatmap(matrix, cmap=colormap, annot=True, fmt=".2f", mask=dropSelf)

    