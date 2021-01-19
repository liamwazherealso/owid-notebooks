# -*- coding: utf-8 -*-
import logging
from pathlib import Path
from glob import glob
from os import path
import os
import pandas as pd
import numpy as np
import pycountry
from itertools import chain
import json



DATASETS = os.path.abspath("../../owid-notebooks/owid-datasets/datasets/")


def get_datapackages_json(dataset,json_package="datapackage.json"):
    """
    returns json data as a dictionary
    :param dataset: directory containing dataset files
    :param json_package: name of json file
    : type str
    :return: json data object as dictionary
    :rtype: dict
    """
    with open("{}/{}".format(os.path.abspath(dataset),json_package), "r") as read_file:
        data = json.load(read_file)
    return data




def generate_datapackage_csv(datasets):
    """returns a dataframe containing data source info

    :param datasets: path to the dataset directory
    :return: Dataframe containing dataset source information
    :rtype: .csv
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
    """converts ountry names to iso3166 codes
    :param ountries: country names
    :type pandas series or list
    :return: ISO3166 country codes
    :rtype: list
    """

    codes = []
    for country in countries:
        try:
            codes.append(pycountry.countries.get(name=country).alpha_3)
        except BaseException:
            codes.append('')
    return codes




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
