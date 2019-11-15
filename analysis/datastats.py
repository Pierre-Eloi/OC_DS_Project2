#! /usr/bin/env python3
# coding: utf-8

""" This module gathers some functions to get some statistics on data. 
"""
import os
import numpy as np
import pandas as pd
from scipy import stats
from IPython.display import display
import statsmodels.api as sm

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
    """ Return a DataFrame with the degrees of freedom and sum of squares as well as residuals
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
        tuple (DataFrame, array of residuals, array of class means)
    """
    x = data[by]
    n = x.size
    n_f = len(columns)
    classes = x.unique()
    k = classes.size
    index = ["SS_total", "SS_model", "SS_error"]
    df = pd.DataFrame([n-1, k-1, n-k], index=index, columns=["DL"])
    E = np.zeros((n, n_f))
    X = np.zeros((n, n_f))
    for i, f in enumerate(columns):
        mu = data[f].mean()
        y = data[f].fillna(mu)
        M = np.zeros((k, 2))
        errors = np.zeros(n)
        means = np.zeros(n)
        for j, c in enumerate(classes):
            y_c = y[x==c]
            idx = y[x==c].nonzero()
            M[j, :] = [y_c.size, y_c.mean()]
            errors[idx] = y_c - y_c.mean()
            means[idx] = y_c.mean()
        SST = np.sum((y.values - mu)**2)
        SSM = np.sum(M[:,0] * (M[:,1] - mu)**2)
        SSE = SST - SSM
        SS = [SST, SSM, SSE]
        df[f] = SS
        E[:, i] = errors
        X[:, i] = means
    return df, E, X

def test_h_anova(data, columns, by):
    """test normality and homoscedasticity hypotheses to validate the ANOVA.
    - normality: Shapiro-Wilk (n<5000) or D’Agostino and Pearson’s
    - homoscedasticity: Breusch-Pagan 
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
    E, X = anova_sum_squares(data, columns, by)[1:]
    n = X.shape[0]
    for i in range(len(columns)):
        resid = E[:, i]
        values = X[:, i].reshape((n, 1))
        # normality test
        if data.shape[0] < 5000:
            n_p = stats.shapiro(resid)[-1] #Shapiro-Wilk
        else:
            n_p = stats.normaltest(resid)[-1] # D’Agostino and Pearson’s
        # homoscedasticity test (Breusch-Pagan)
        h_p = sm.stats.diagnostic.het_breuschpagan(resid, values)[-1]
        if i == 0:
            df = pd.DataFrame({columns[i]: np.array([n_p, h_p])},
                              index=["normality_pv", "homocedasticity_pv"])
        else:
            df[columns[i]] = np.array([n_p, h_p])
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
        tuple (DataFrame with SS, DataFrame with hypotheses test results, DataFrame with ANOVA results) 
    """
    df = anova_sum_squares(data, columns, by)[0]
    h_test = test_h_anova(data, columns, by)
    features = df.columns[1:].tolist()
    index = ['eta_2', 'F', 'p']
    test = pd.DataFrame(np.zeros((3, len(features))), index=index, columns=features)                       
    for var in features:
        eta_2 = df[var][1] / df[var][0] 
        F = (df[var][1]/df.iloc[1, 0]) / (df[var][2]/df.iloc[2, 0])
        p = stats.f.sf(F, df.iloc[1, 0], df.iloc[2, 0])
        test[var] = [eta_2, F, p]
    display(df)    
    display(test)
    display(h_test)
    return df, h_test, test