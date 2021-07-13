import os
from typing import List, Dict
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re


def to_snake_case(str_list: List[str]) -> list:
    """
    formats list of strings to snake case
    :param str_list: a list of strings we want to convert to snake case
    :return: a list of strings in snake case
    """
    return [str_.lower().replace(' ', '_') for str_ in str_list]


class DataPipe:
    """
    Class to manage data preprocessing for Freddie Mac loan level data.

    Parameters
    ----------
    headers: Dict[str, List[str]]
            The headers used to.
    directory: str
            The path to a folder holding all the Freddie Mac data.
    """

    def __init__(self, directory: str, headers: Dict[str, List[str]]):
        self.raw_data = self.append_all_files_as_df(directory, headers)

    @staticmethod
    def append_all_files_as_df(directory, headers):
        """
        Runs at initialization--builds two dataframes from the time series and origination data in the target folders.
        The directory must break out the
        :param directory:
        :param headers:
        :return:
        """
        df_time_series = pd.DataFrame()
        df_origination = pd.DataFrame()
        print(os.walk(directory))
        for path_object in os.walk(directory):
            print(path_object)
            folder = path_object[0]
            for file in path_object[2]:
                relative_path = folder + '/' + file
                if file.find('excl') == -1:
                    header = headers['origination']
                    df_origination_appender = pd.read_csv(relative_path
                                                          , names=header
                                                          , index_col=False
                                                          , sep='|')
                    df_origination.append(df_origination_appender)
                else:
                    header = headers['time_series']
                    df_time_series_appender = pd.read_csv(relative_path
                                                          , names=header
                                                          , index_col=False
                                                          , sep='|')
                    df_time_series.append(df_time_series_appender)

        return {'time_series': df_time_series
            , 'origination': df_origination}

    def clean(self):
        """
        Executes the provided sql query.

        Parameters
        ----------
        sql_query: SqlQuery or None
            If None--defaults to the original sql query given. The only reason an additional sql query is given is
            to break up the date range after a Java Heap error--this tends to be from trying to collect too much data
            at once.

        Returns
        -------
        spark.sql.DataFrame object defined by our data and the sql query that is ran against that data.
        """
        pass


if __name__ == '__main__':
    # defined in the SFLLD User Guide
    # http://www.freddiemac.com/fmac-resources/research/pdf/user_guide.pdf
    time_series_headers = ['LOAN SEQUENCE NUMBER', 'MONTHLY REPORTING PERIOD'
        , 'CURRENT ACTUAL UPB', 'CURRENT LOAN DELINQUENCY STATUS'
        , 'LOAN AGE', 'REMAINING MONTHS TO LEGAL MATURITY'
        , 'REPURCHASE FLAG', 'MODIFICATION FLAG'
        , 'ZERO BALANCE CODE', 'CURRENT INTEREST RATE'
        , 'CURRENT DEFERRED UPB', 'DUE DATE OF LAST PAID INSTALLMENT (DDLPI)'
        , 'MI RECOVERIES', 'NET SALES PROCEEDS', 'NON MI RECOVERIES'
        , 'EXPENSES', 'LEGAL COSTS', 'MAINTENANCE AND PRESERVATION COSTS'
        , 'TAXES AND INSURANCE', 'MISCELLANEOUS EXPENSES'
        , 'ACTUAL LOSS CALCULATION', 'MODIFICATION COST'
        , 'STEP MODIFICATION FLAG', 'DEFERRED PAYMENT PLAN'
        , 'ESTIMATED LOAN TO VALUE (ELTV)', 'ZERO BALANCE REMOVAL UPB'
        , 'DELINQUENT ACCRUED INTEREST', 'DELINQUENCY DUE TO DISASTER'
        , 'BORROWER ASSISTANCE STATUS CODE', 'CURRENT MONTH MODIFICATION COST']
    origination_headers = []

    time_series_headers_adjusted = to_snake_case(time_series_headers)
    origination_headers_adjusted = to_snake_case(origination_headers)

    headers_dict = {'time_series': time_series_headers_adjusted
        , 'origination': origination_headers_adjusted}

    dir_ = '../../data/'

    datapipe = DataPipe(dir_, headers_dict)
    print([folder_obj for folder_obj in os.walk(dir_)])
    print(datapipe.raw_data['time_series'].head())

    pass
