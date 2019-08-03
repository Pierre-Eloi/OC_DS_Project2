#! /usr/bin/env python3
# coding: utf-8

""" This module gathers all functions required for
downloading and loading data. 
"""

import os
from zipfile import ZipFile
from six.moves import urllib
import pandas as pd
from IPython.display import display

def download_data(url, data_name='data', data_folder='datasets'):
    """Download data from an url.
    Parameters
    ----------
    url: url of the site hosting data
    data_name: name of the zip folder containing downloaded data
    data_folder: name of the project directory gathering data
    Returns
    -------
    list object
        List gathering the name of all dowloaded files
    """
    folder_path=os.path.join(data_folder)
    if not os.path.isdir(folder_path):
        os.makedirs(folder_path)
        data_path = os.path.join(folder_path, data_name + ".zip")
        urllib.request.urlretrieve(url, data_path)
        with ZipFile(data_path, 'r') as data_zip:
            data_zip.extractall(path=folder_path)
    files = []
    # list all extracted files 
    for r, d, f in os.walk(folder_path): # r=root, d=directories, f=files
        for file in f:
            files.append(file)
    print("The extracted files are:")
    for f in files:
        print(f)
    return files

def load_data(csv_file):
    """ Load .csv files into a dataframe.
    Display also the first 3 rows.
        Parameters
    ----------
    csv_file: str object
        name of the csv file to be loaded (with .csv extension)
    Returns
    -------
    DataFrame
        A comma-separated values (csv) file is returned as two-dimensional
        data structure with labeled axes.
    """
    csv_path = os.path.join('datasets', csv_file)
    df = pd.read_csv(csv_path)

    display(df.head(3))
    return df
