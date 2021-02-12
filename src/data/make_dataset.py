# -*- coding: utf-8 -*-
import click
import logging
import os
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from glob import glob
from os import path
from itertools import chain 

import pandas as pd
import numpy as np

DATASETS_PATH = "../../owid-datasets/datasets/"

def load_dataset(dsName):
    """Load dataset with provided name

    Parameters
    ----------
    dsName : str
        name of dataset

    Returns
    -------
    DataFrame
        DataFrame loaded from csv path.
    """
    dataset_path = os.path.join(DATASETS_PATH, dsName, dsName + ".csv")

    return pd.read_csv(dataset_path)

def gen_dsName_to_dtypes():
    """Generate dict mapping ds name to dtypes.

    Returns
    -------
    dict
        maps dataset name to dtypes
    """
    dsName_to_dtypes = {}
    
    datasets_path = glob(DATASETS_PATH + '*')

    for dsName in datasets_path:
        ds = os.path.basename(dsName)
        df = load_dataset(ds)
        dsName_to_dtypes[ds] = df.dtypes
    return dsName_to_dtypes

def get_df_cols(dsName_to_dtypes):
    """
    Parameters
    ----------
    dsName_to_dtypes : dict
        dict from dsName to dtypes

    Returns
    -------
    dict
        dataframe where index is the dataset, columns are all the fields in every dataset, column values are what dtype the column is.
    """

    y_dim =  set((chain(*[dtypes.index for dtypes in dsName_to_dtypes.values()])))
    x_dim = dsName_to_dtypes.keys()
    df_cols = pd.DataFrame(index=x_dim, columns=y_dim)
    df_cols = df_cols.astype('object')
    # enter rows to df_cols from dsName_to_dtypes. 
    for ds, cols in dsName_to_dtypes.items():
        cols = cols.astype('object')
        df_cols.loc[ds, cols.index] = cols
    return df_cols

def get_col_to_uniq(df_cols):
    """
    Parameters
    ----------
    df_cols : dict
        dict from dsName to dtypes

    Returns
    -------
    dict
        maps from column name to list of unique values
    """
    # gather conflict columns: where there are more than 2 unique values in a column
    s = df_cols.describe(include='all').loc['unique', :]
    s = s[s > 1]
    
    # gather unique values from columns
    col_to_uniq = {}
    for c in s.index:
        col_to_uniq[c] = df_cols.loc[:, c].unique()
    return col_to_uniq

def get_col_to_dtype(col_to_uniq, hierarchy=None):
    """ get dtype according to hierarchy per column

    Parameters
    ----------
    col_to_uniq : dict
        maps from column name to list of unique values

    hierarchy : list, optional
        change default hierarchy
    Returns
    -------
    dict
        map from column to dtype picked by hierarchy
    """
    if hierarchy is None:
        hierarchy = ["object", "float64", "int64", "nan"]
        
    # apply hierarchy to conflict columns
    col_to_dtype = {}
    for col, uniq in col_to_uniq.items():
        col_to_dtype[col] = hierarchy[min([hierarchy.index(str(v)) for v in uniq])]
    return col_to_dtype

def apply_data_hierarchy(df, col_to_dtype, overwrite={}):
    """ apply a data hierarchy on a dataframe

    Parameters
    ----------
    df : DataFrame
        DataFrame to apply dtype change to
    Returns
    -------
    DataFrame
        DataFrame with new column dtypes
    """
    if not any([str(col) in col_to_dtype for col in df.columns]):
        return df
    
    # create sub_dict from data_hierarchy
    for k,v in overwrite.items():
        col_to_dtype[k] = v
 
    w = {col: col_to_dtype[col] for col in df.columns if col in col_to_dtype}


    return df.astype(w)

def consolidate():
    """consolidate owid-datasets into single dataframe
    """
    dsName_to_dtypes = gen_dsName_to_dtypes()
    df_cols = get_df_cols(dsName_to_dtypes)
    col_to_uniq = get_col_to_uniq(df_cols)
    col_to_dtype = get_col_to_dtype(col_to_uniq)

    overwrite = {'Forest Transition Phase': 'object'}

    # do while prevents creating a 
    do_while = 0
    for ds in glob(DATASETS_PATH+'*'):
        do_while += 1
        if do_while == 1:
            ds = os.path.basename(ds)
            df = load_dataset(ds)
            df = df.set_index(["Entity", "Year"])
            df = apply_data_hierarchy(df, col_to_dtype, overwrite=overwrite)
            continue
            
        ds = os.path.basename(ds)
        df2 = load_dataset(ds)
        df2 = df2.set_index(["Entity", "Year"])
        
        overwrite['ds_name'] = ds
        df2 = apply_data_hierarchy(df2, col_to_dtype, overwrite=overwrite)
        
        try:
            df = pd.merge(df, df2, how='left', on=["Entity", "Year"])
        except ValueError:
            print("MergeError:", ds)

    # Workaround for failed data set
    df2 = load_dataset('Cumulative share of marriages ending in divorce (England and Wales, UK ONS)')
    retry_df = apply_data_hierarchy(df2, col_to_dtype, overwrite={"Year": "object"})
    pd.merge(df, retry_df, how='left', on=["Entity", "Year"])

    df.to_csv('../../data/processed/owid-datasets.csv')

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    consolidate()
