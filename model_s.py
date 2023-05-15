from getdata import YahooFinance
from getdata import SQLrepo

import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

from sklearn.metrics import mean_absolute_error

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.ar_model import AutoReg

from dateutil.parser import parse

from tqdm import tqdm

import warnings
from statsmodels.tools.sm_exceptions import ValueWarning, HessianInversionWarning, ConvergenceWarning
warnings.simplefilter(action="ignore", category=FutureWarning)
warnings.filterwarnings('ignore', category=ValueWarning)
warnings.filterwarnings('ignore', category=HessianInversionWarning)
warnings.filterwarnings('ignore', category=ConvergenceWarning)


db_name = "stocks.sqlite"


class StockModel():
    """ StockModel Class for training and testing the model
        >>> model = StockModel(table_name="AAPL")
        Methods:
            model.prp_model_data(returns=True) # returns the data with returns ratio
            model.train_model(cut=0.8, returns=True) # returns the y_pred_wfv
            model.plot_pred # returns the plot
            model.y_test # returns the y_test
            model.trained_model # returns the trained model
            model.preds_actual # returns the pred_actual df
            model.test_mae # returns the test_mae
            model.training_base # returns the training_base Mae

    """

    def __init__(self, table_name, order=(6, 0, 0)):
        """Init the class"""
        self.table_name = table_name
        self.order = order
        self.connection = sqlite3.connect(
            database=db_name, check_same_thread=False)
        self.repo = SQLrepo(connection=self.connection)

    def prp_model_data(self, returns=True):
        """Prepare the data for the model

        Args:
            returns (bool, optional): Prepare the data for the model with returns ratio. Defaults to True.

        Returns:
            Pd.Series: Ts wis dates and returns or close prices
        """

        # this limit for test only and will be changed to None
        df_data = self.repo.read_table(table_name=self.table_name)

        df_data['Date'] = pd.to_datetime(
            df_data['Date'].str.replace(r'-\d{2}:\d{2}$', '', regex=True))

        df_data.set_index('Date', inplace=True)

        # resampling method is soOoOooo  IMPORTANT "b" or "c"  check pandas Docs for it
        df_prices = df_data.resample('b').ffill().squeeze()
        df_returns = df_prices.pct_change().dropna()

        if returns:
            self.df_returns = df_returns
            return self.df_returns
        else:
            self.df_prices = df_prices
            return self.df_prices

    def train_model(self, cut=0.8, returns=True):
        """ Train the model with Walk Forward Validation

        Args:
            cut (float, optional): Cut the data to train and test. Defaults to 0.8.
            returns (bool, optional): Train the model with returns ratio. Defaults to True.

        >>> model = StockModel(table_name="AAPL")
        >>> model.train_model(cut=0.8, returns=True)

        Methods:




        """

        # split the data to y_train , y_test

        data = self.prp_model_data(returns=returns)

        cut_off = int(len(data) * cut)

        y_train = data.iloc[:cut_off]

        y_test = data.iloc[cut_off:]

        # wfv
        y_pred_wfv = pd.Series()
        history = y_train.copy()
        print(
            f"Starting {self.table_name} training Arima{self.order} with Returns { bool(returns)}")
        print(
            f"Performing Walk Forward Val.. for {len(y_test)} OBS with trained==> {len(data)}")
        print(f"Null Values Check ====> {data.isna().sum()}")
        for i in tqdm(range(len(y_test))):
            model = ARIMA(history, order=self.order).fit()
            next_pred = model.forecast()
            y_pred_wfv = y_pred_wfv.append(next_pred)
            history = history.append(y_test[next_pred.index])

        # save the model for future use and evaluation
        self.trained_model = model
        self.training_base = mean_absolute_error(
            y_train, [y_train.mean()] * len(y_train))
        self.test_mae = mean_absolute_error(y_test, y_pred_wfv)

        # append the last 3 predictions to the y_pred_wfv
        y_pred_wfv = y_pred_wfv.append(self.trained_model.forecast(3))

        # Concatenate the y_test and y_pred_wfv with

        df_pred = pd.concat([y_test, y_pred_wfv], axis=1)
        df_pred.columns = ['y_test', 'y_pred']

        fig = px.line(df_pred, labels={"Returns"},
                      title="Predictions Vs Actual Returns")

        # save the data for future use and evaluation

        self.y_test = y_test
        self.preds_actual = df_pred
        self.preds = y_pred_wfv
        prices = self.prp_model_data(returns=False).iloc[cut_off:]
        self.prices = prices.drop(prices.index[0])
        self.plot_pred = fig.update_layout(
            xaxis_title="Date", yaxis_title="Returns")

        print(f"=========== {self.table_name} Training Ends ===========")
        print(
            f"Test MAE ==> {self.test_mae}\nTraining Baseline==> {self.training_base}")
        return

    def insert_pred_table(self):
        """
        Insert records into a table
        Args:
            table_name: name of the table to insert records
            records: records to insert into the table --> pandas dataframe from yahoo finance
        Returns:
            str : message of the operation "{Table Name} inserted successfully"
        """
        table_name = f"{self.table_name}_pred"
        records = self.preds_actual
        self.repo.insert_table(table_name=table_name, records=records)
        return f"{table_name} inserted successfully"
