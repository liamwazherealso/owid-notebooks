# -*- coding: utf-8 -*-
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from glob import glob
from os import path
import os
import pandas as pd
import numpy as np
import pycountry
from itertools import chain
import json


DATASETS = os.path.abspath("../../owid-notebooks/owid-datasets/datasets/")


def get_datapackages_json(dataset):
    """
    returns a dictionary given a path to a .json file

    Args: datasets :path do individual datasets
    ----
    """

    with open("{}/datapackage.json".format(os.path.abspath(dataset)), "r") as read_file:
        data = json.load(read_file)
    return data


def parse_dict(string, data, strings=None):
    """
    brute force attempt at checking each string value in a JSON file that contains a substring
    *********Work in progress**************

    """
    if not string:
        strings = ''
    if isinstance(data, dict):
        for key, value in data.items():
            parse_dict(string, value, strings)
    elif isinstance(data, str):
        if string in data:
            strings += data
    elif isinstance(data, set):
        for ind in data:
            parse_dict(string, data, strings)

    elif isinstance(data, list):
        for ind in data:
            parse_dict(string, data, strings)
    else:
        pass
    return strings


def generate_datapackage_csv(datasets):
    """
    returns a dataframe containing the links to source data for each data.package.json

    Args: datasets :path do individual datasets
    ----
    """
    headers = ['id', 'publisher', 'title', 'source_links']
    body = []
    for dataset in glob(datasets + '/*'):
        data = get_datapackages_json(dataset)
        http_list = None
        try:
            http_list = data['sources'][0].get('link')
        except BaseException:
            pass
        try:
            dataset_publisher = data['sources'][0].get('dataPublisherSource')
        except BaseException:
            pass

        dataset_id = data['id']
        dataset_title = data['title']

        body.append([dataset_id, dataset_publisher, dataset_title, http_list])
    df = pd.DataFrame(columns=headers, data=body)
    return df


def get_iso3code(countries):
    """
    returns a list of ISO 3166 country codes from a given list of countries
    Args: countries: country names

    Returns: list of ISO3166 country codes

    """
    codes = []
    for country in countries:
        try:
            codes.append(pycountry.countries.get(name=country).alpha_3)
        except BaseException:
            codes.append('')
    return codes


def get_ds_dict(datasets):
    """
    returns a dictionary of dtypes in each csv given a directory of subdirectories containing csvs
    """
    ds_dict = {}
    for ds in glob(datasets + '/*'):
        ds = os.path.basename(ds)
        df = load_data(ds)
        ds_dict[ds] = df.dtypes
    return ds_dict


def load_data(ds):
    """returns dataframe diven a dataset directory """
    return pd.read_csv(os.path.join(DATASETS, ds, ds + ".csv"))


def get_df_cols(ds_dict):

    y_dim = set((chain(*[dtypes.index for dtypes in ds_dict.values()])))
    x_dim = ds_dict.keys()
    df_cols = pd.DataFrame(index=x_dim, columns=y_dim)
    df_cols = df_cols.astype('object')
    # enter rows to df_cols (index is the dataset, columns are all the fields
    # in every dataset, column values are what dtype the column is) from
    # ds_dict.
    for ds, cols in ds_dict.items():
        cols = cols.astype('object')
        df_cols.loc[ds, cols.index] = cols
    return df_cols


def get_col_to_uniq(df_cols):
    """ returns map from """
    # gather conflict columns: where there are more than 2 unique values in a
    # column
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
        col_to_dtype[col] = hierarchy[min(
            [hierarchy.index(str(v)) for v in uniq])]
    return col_to_dtype


def apply_data_hierarchy(df, col_to_dtype, overwrite={}):
    """ apply a data hierarchy on a dataframe
    """
    if not any([str(col) in col_to_dtype for col in df.columns]):
        return df

    # create sub_dict from data_hierarchy
    for k, v in overwrite.items():
        col_to_dtype[k] = v

    w = {col: col_to_dtype[col] for col in df.columns if col in col_to_dtype}
    return df.astype(w)


def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')


country_names = ['Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia',
                 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain',
                 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin',
                 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina',
                 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso',
                 'Burundi', 'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada',
                 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia',
                 'Comoros', 'Congo', 'Cook Islands', 'Costa Rica', "Cote d'Ivoire",
                 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic',
                 'Democratic Republic of Congo', 'Denmark', 'Djibouti', 'Dominica',
                 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador',
                 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Fiji',
                 'Finland', 'France', 'French Polynesia', 'Gabon', 'Gambia',
                 'Georgia', 'Germany', 'Ghana', 'Greece', 'Greenland', 'Grenada',
                 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti',
                 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India',
                 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy',
                 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati',
                 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho',
                 'Liberia', 'Libya', 'Lithuania', 'Luxembourg', 'Macedonia',
                 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta',
                 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico',
                 'Micronesia (country)', 'Moldova', 'Mongolia', 'Montenegro',
                 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal',
                 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria',
                 'Niue', 'North Korea', 'Norway', 'Oman', 'Pakistan', 'Palau',
                 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru',
                 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar',
                 'Romania', 'Russia', 'Rwanda', 'Saint Kitts and Nevis',
                 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa',
                 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia',
                 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia',
                 'Solomon Islands', 'Somalia', 'South Africa', 'South Korea',
                 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Swaziland', 'Sweden',
                 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania',
                 'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga',
                 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan',
                 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan',
                 'Vanuatu', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia',
                 'Zimbabwe']

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())
