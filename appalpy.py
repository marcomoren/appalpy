#!/usr/bin/env python

from appalpy_funcs import *
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from urllib.error import HTTPError

class Tenders():
    """
    This class is used to structure the dataset containing the data, returning it as a DataFrame filtered
    according to the user's input.
    """
    def __init__(self, start=None, end=None,  contracting_entity=None, scope_keywords=None):

        # Start date is set equal to user's input where specified. Otherwise it is set equal to one year ago today.  
        if start is not None:
            self.start = datetime(int(start[:4]),int(start[5:7]),int(start[-2:]))
        else:
            self.start = datetime.combine(date.today() + relativedelta(years=-1), datetime.min.time())
        
        # End date is set equal to user's input where specified. Otherwise it is set equal to today's date.
        if end is not None:
            self.end = datetime(int(end[:4]),int(end[5:7]),int(end[-2:]))
        else:
            self.end = datetime.combine(date.today(), datetime.min.time())
        self.contracting_entity = contracting_entity
        self.scope_keywords = scope_keywords

    def get_tenders(self):
        
        #This method generates the dataframe containing all public tenders for the selected period and reduce it according to the 
        # rules specified by the user (if any)
        master_df = pd.DataFrame()
        for period in periods(self.start, self.end):
            try:
                tender_data = get_tender_data(period)
                if self.contracting_entity is not None:
                    tender_data = reduce_data(tender_data, keywords=self.contracting_entity, field="denominazione_amministrazione_appaltante")
                else:
                    pass
                if self.scope_keywords is not None:
                    tender_data = reduce_data(tender_data, keywords=self.scope_keywords, field="oggetto_lotto")
                else:
                    pass
                master_df = master_df.append(tender_data)
                print(period)
                print("done")
            except HTTPError:
                pass
        master_df["data_pubblicazione"] = pd.to_datetime(master_df["data_pubblicazione"])
        master_df.drop(master_df[master_df["data_pubblicazione"] < self.start].index, inplace=True)
        master_df.drop(master_df[master_df["data_pubblicazione"] > self.end].index, inplace=True)
        return master_df

    def get_contractor_info(self):
        
        # This method returns a DataFrame containing data on contractor
        contractor = get_contractor_data()
        awards = get_awards_data()
        contractor_info = pd.merge(contractor, awards, on="id_aggiudicazione", how="inner")
        for col in contractor_info.columns:
            if col[-2:] == "_x":
                newcol = col[:-2]
                contractor_info = contractor_info.rename({col : newcol}, axis="columns")
            elif col[-2] == "_" and col[-1] != "x":
                contractor_info = contractor_info.drop(col, axis=1)
            else:
                pass
        return contractor_info

    def get_data(self):

        # This method merges the DataFrames obtained with the previous methods, providing the user with a complete dataset
        # with information on published public tenders, participation, awarding process and selected contractors.
        tenders = self.get_tenders()
        awards = get_awards_data()
        td = tenders.merge(awards, on="cig", how="inner")
        cd = get_contractor_data()
        data = td.merge(cd, on="id_aggiudicazione", how="inner")
        for col in data.columns:
            if col[-2:] == "_x":
                newcol = col[:-2]
                data = data.rename({col : newcol}, axis="columns")
            elif col[-2] == "_" and col[-1] != "x":
                data = data.drop(col, axis=1)
            else:
                pass
        return data