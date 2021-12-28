#!/usr/bin/env python

from datetime import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
from typing import Union

def ymformat(date:datetime):
    """
    This function generates a string containing year and month to be used to access the relevant URL (e.g., "2021_07")
    """
    ymformat = str(date)[:7].replace("-","_")
    return ymformat


def periods(start:datetime, end:datetime):
    """
    This function generates a list of years and months between the starting and ending dates (inclusive) selected by the user.
    Such list is used to iterate through the relevant URLs.  
    """
    periods_list = []
    moving_period = start
    while moving_period <= end.replace(day=1):
        periods_list.append(moving_period)
        moving_period = moving_period + relativedelta(months=+1)
    return periods_list

def get_tender_data(date:datetime):
    """
    This function opens the intended URL containing data on monthly tenders, opens the csv dataset contained inside the downloadable zip file 
    and generates a pandas DataFrame.
    """
    base_url = "https://dati.anticorruzione.it/opendata/download/dataset/cig-"
    full_url = base_url + ymformat(date)[:4] + "/filesystem/cig_csv_" + ymformat(date) + ".zip"
    #requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS='ALL'
    #requests.packages.urllib3.contrib.pyopenssl.extract_from_urllib3()
    tender_csv_file = pd.read_csv(full_url, compression='zip', sep=';', dtype='object')
    return tender_csv_file

def get_awards_data():
    """
    This function opens the URLs cointaining data on tender awards, opens the csv dataset contained inside the downloadable zip file and 
    generates a pandas DataFrame.
    """
    awards_url = "https://dati.anticorruzione.it/opendata/download/dataset/aggiudicazioni/filesystem/aggiudicazioni_csv_0.zip"
    awards_csv_file = pd.read_csv(awards_url, compression='zip', sep=';', dtype='object')
    return awards_csv_file

def get_contractor_data():
    """
    This function opens the URLs cointaining data on contractor companies, opens the csv dataset contained inside the downloadable zip file 
    and generates a pandas DataFrame.
    """
    contractor_url = "https://dati.anticorruzione.it/opendata/download/dataset/aggiudicatari/filesystem/aggiudicatari_csv_0.zip"
    contractor_csv_file = pd.read_csv(contractor_url, compression='zip', sep=';', dtype='object')
    return contractor_csv_file

def reduce_data(df, keywords:Union[list, str], field:str):
    """
    This function reduces the dataset based on conditions provided by the user
    """
    if type(keywords) is list:
        df = df[df[field].str.contains("|".join(keywords).lower(), case=False, na = False)]
    elif type(keywords) is str:
        df = df[df[field].str.contains(keywords.lower(), case=False, na = False)]
    else:
        raise TypeError("user input must be passed as a list or a string")
    return df