import os
from typing import List
import pandas as pd


def to_snake_case(str_list: List[str]) -> list:
    """
    formats list of strings to snake case
    :param str_list: a list of strings we want to convert to snake case
    :return: a list of strings in snake case
    """
    return [str_.lower().replace(' ', '_') for str_ in str_list]


class DataPipeXY:
    """
    Datapipe for predicting if a loan will ever go over 90 days late on its payments from origination data. This
    class builds X and y for the dataset where X is the data for learning and y is the target variable 1 or 0;
    1 if the loan has ever been over 89 days late, and zero otherwise.
    """

    def __init__(self):
        # hardcoded col names for the txt files we load in.
        self.X_header = to_snake_case(['CREDIT SCORE', 'FIRST PAYMENT DATE', 'FIRST TIME HOMEBUYER FLAG'
        , 'MATURITY DATE', 'METROPOLITAN STATISTICAL AREA (MSA) OR METROPOLITAN DIVISION'
        , 'MORTGAGE INSURANCE PERCENTAGE (MI %)', 'NUMBER OF UNITS'
        , 'OCCUPANCY STATUS', 'ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)'
        , 'ORIGINAL DEBT-TO-INCOME (DTI) RATIO', 'ORIGINAL UPB'
        , 'ORIGINAL LOAN-TO-VALUE (LTV)', 'ORIGINAL INTEREST RATE'
        , 'CHANNEL', 'PREPAYMENT PENALTY MORTGAGE (PPM) FLAG', 'AMORTIZATION TYPE'
        , 'PROPERTY STATE', 'PROPERTY TYPE', 'POSTAL CODE', 'LOAN SEQUENCE NUMBER'
        , 'LOAN PURPOSE', 'ORIGINAL LOAN TERM', 'NUMBER OF BORROWERS'
        , 'SELLER NAME', 'SERVICER NAME', 'SUPER CONFORMING FLAG'
        , 'Pre-HARP LOAN SEQUENCE NUMBER', 'PROGRAM INDICATOR', 'HARP INDICATOR'
        , 'PROPERTY VALUATION METHOD', 'INTEREST ONLY INDICATOR (I/O INDICATOR)'
                           ])
        self.y_header = to_snake_case(['LOAN SEQUENCE NUMBER', 'MONTHLY REPORTING PERIOD'
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
        , 'BORROWER ASSISTANCE STATUS CODE', 'CURRENT MONTH MODIFICATION COST'
                           ])
        self.use_cols_y = ['current_loan_delinquency_status', 'loan_sequence_number']

        self.X = None
        self.y = None
        self.Xy = None

    def build_x(self, directory):
        header = self.X_header
        df_origination = pd.DataFrame()

        for path_object in os.walk(directory):
            folder = path_object[0]
            for file in path_object[2]:
                if file[-4:] == '.txt':
                    relative_path = folder + '/' + file
                    if file.find('time') == -1:
                        print('origination:', file)
                        df_origination_appender = pd.read_csv(relative_path
                                                              , names=header
                                                              , index_col=False
                                                              , sep='|')
                        df_origination = df_origination.append(df_origination_appender)
        self.X = df_origination

    def build_y(self, directory):
        """
        Navigates all sub directories looking for time series data, then determines if a loan has ever been
        over n days late. n is currently set at 90 days via: x in ['0', '1', '2']
        :return: a dict with the account id as the key, and the value 1 or 0 determining if that account
                 has ever been 90 days late or more.
        """
        use_cols = self.use_cols_y
        header = self.y_header
        y = {}
        days_late_values = ['0', '1', '2'] # see freddie mac data dictionary
        for path_object in os.walk(directory):
            folder = path_object[0]
            for file in path_object[2]:
                if file[-4:] == '.txt':
                    relative_path = folder + '/' + file
                    if file.find('time') != -1:
                        print('time series:', file)
                        df_time_series = pd.read_csv(relative_path
                                                      , names=header
                                                      , index_col=False
                                                      , sep='|'
                                                      , usecols=use_cols)
                        df_gb = df_time_series.groupby('loan_sequence_number')
                        for name, group in df_gb:
                            if name in y.keys():
                                if y[name] == 1:
                                    continue
                            if all(status in days_late_values for status in group['current_loan_delinquency_status']):
                                delinquent = 0
                            else:
                                delinquent = 1
                            y[name] = delinquent
                        del df_time_series, df_gb  # ensures garbage collection (I think)
        self.y = y

    def build_xy(self):
        """
        Matches the correct outcome (target variable) to the independent data.
        :return: sets attribute Xy
        """
        X = self.X.copy()
        y = self.y
        if y is None:
            raise ValueError('y has not been set yet')

        X['target'] = X['loan_sequence_number'].map(y)

        self.Xy = X

    @staticmethod
    def export_csv(data: pd.DataFrame, path: str):
        """
        Exports dataframe as a csv.
        :param data: data to upload as a csv
        :param path: where to upload the csv
        :return:
        """
        data.to_csv(path)


class Preprocessor:
    """
    Not finished
    """
    def __init__(self, data, transformations, nulls, dimensionality_reduction, dummy_variables):
        self.data = data
        self.transformations = transformations
        self.nulls = nulls
        self.dimensionality_reduction = dimensionality_reduction
        self.dummy_variables = dummy_variables
        self.outliers = None
        pass


class ClassificationModelExperiment:
    """
    Not finished
    Class to guide model development. Accepts a handful of parameters useful in determining what type of models,
    preprocessing, hyperparams, etc impact performance.
    """
    def __init__(self, X: pd.DataFrame, y: pd.DataFrame, models: List
                 , preprocessing: Preprocessor, imbalanced_learning: list, sample_size: int):
        self.X = X
        self.y = y
        self.sample_size = sample_size
        self.preprocessing = preprocessing
        self.imbalanced_learning = imbalanced_learning
        self.models = models
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.trained_models = None

    def preprocess(self):
        pass

    def train_test_split(self):
        # class imbalances
        pass

    def test_models(self):
        pass

    def train_models(self):
        pass

    def score_models(self):
        pass


if __name__ == '__main__':
    pass
