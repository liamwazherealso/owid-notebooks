# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from glob import glob
from os import path
import os
import pandas as pd
import numpy as np


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())

DATASETS = "../owid-datasets/datasets/*"

def load_data(ds):
    return pd.read_csv(os.path.join("../owid-datasets/datasets/", ds, ds + ".csv"))
    main()
# consolidate code: dtype hierarchy. 


# create empty df to insert the dtypes for each
from itertools import chain 


def get_ds_dict():
    ds_dict = {}
    for ds in glob(DATASETS):
        ds = os.path.basename(ds)
        df = load_data(ds)
        ds_dict[ds] = df.dtypes
    return ds_dict

        
def get_df_cols(ds_dict):
    y_dim =  set((chain(*[dtypes.index for dtypes in ds_dict.values()])))
    x_dim = ds_dict.keys()
    df_cols = pd.DataFrame(index=x_dim, columns=y_dim)
    df_cols = df_cols.astype('object')
    # enter rows to df_cols (index is the dataset, columns are all the fields in every dataset, column values are what dtype the column is) from ds_dict. 
    for ds, cols in ds_dict.items():
        cols = cols.astype('object')
        df_cols.loc[ds, cols.index] = cols
    return df_cols


def get_col_to_uniq(df_cols):
    """ returns map from """
    # gather conflict columns: where there are more than 2 unique values in a column
    s = df_cols.describe(include='all').loc['unique', :]
    s = s[s > 1]
    
    # gather unique values from columns
    col_to_uniq = {}
    for c in s.index:
        col_to_uniq[c] = df_cols.loc[:, c].unique()
    return col_to_uniq
        
def get_col_to_dtype(col_to_uniq, hierarchy=None):
    """ get dtype hierarchy per column
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
    """
    if not any([str(col) in col_to_dtype for col in df.columns]):
        return df
    
    # create sub_dict from data_hierarchy
    for k,v in overwrite.items():
        col_to_dtype[k] = v
 
    w = {col: col_to_dtype[col] for col in df.columns if col in col_to_dtype}


    return df.astype(w)

def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())