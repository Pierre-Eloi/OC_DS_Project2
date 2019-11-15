#! /usr/bin/env python3
# coding: utf-8

""" This module gathers some functions to get some statistics on data. 
"""
import os
import numpy as np
import pandas as pd
from scipy import stats
from IPython.display import display

def na_count(data):
    """Give the number of NaN for each features
    -----------
    Parameters :
    data: DataFrame
        the pandas object holding the data
        -----------
    Return :
        DataFrame
    """
    features = data.columns
    n = data.shape[0]
    n_null = n - data.count()
    ratio = round(n_null/n*100, 1)
    return pd.DataFrame({"NaN_number": n_null, "NaN_ratio_%": ratio}, index=features)

def anova_sum_squares(data, columns, by):
    """ Return a DataFrame with the degrees of freedom and sum of squares
    -----------
    Parameters :
    data: DataFrame
        the pandas object holding the data
    columns: list
        list of names of numerical feature
    by: string
        name of the categorical feature
        -----------
    Return :
        DataFrame
    """
    x = data[by]
    n = x.size
    classes = x.unique()
    k = classes.size
    index = ["SS_total", "SS_model", "SS_error"]
    df = pd.DataFrame([n-1, k-1, n-k], index=index, columns=["DL"])
    for f in columns:
        mu = data[f].mean()
        y = data[f].fillna(mu)
        M = np.zeros((k, 2))
        for j, c in enumerate(classes):
            y_c = y[x==c]
            M[j,:] = [y_c.size, y_c.mean()]
        SST = np.sum((y.values - mu)**2)
        SSM = np.sum(M[:,0] * (M[:,1] - mu)**2)
        SSE = SST - SSM
        SS = [SST, SSM, SSE]
        df[f] = SS
    display(df)
    return df

def anova_Ftest(data, columns, by):
    """ Return a DataFrame with the F-Test Results of the ANOVA:
    1. eta_2
    2. F-test
    3. p value
    -----------
    Parameters :
    data: DataFrame
        the pandas object holding the data
    columns: list
        list of names of numerical feature
    by: string
        name of the categorical feature
    -----------
    Return :
        DataFrame
    """
    df = anova_sum_squares(data, columns, by)
    features = df.columns[1:].tolist()
    index = ['eta_2', 'F', 'p']
    test = pd.DataFrame(np.zeros((3, len(features))), index=index, columns=features)                       
    for var in features:
        eta_2 = df[var][1] / df[var][0] 
        F = (df[var][1]/df.iloc[1, 0]) / (df[var][2]/df.iloc[2, 0])
        p = stats.f.sf(F, df.iloc[1, 0], df.iloc[2, 0])
        test[var] = [eta_2, F, p]
    display(test)