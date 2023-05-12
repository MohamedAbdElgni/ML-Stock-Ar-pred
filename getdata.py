from typing import Any

import yfinance as yf

import pandas as pd



class YahooFinance:
    """
    Class to get data from Yahoo Finance API

    """

    def __init__(self, ticker: str):
        """
        param ticker: ticker of the stock to get data
        >>> YahooFinance('AAPL')
        """

        self.ticker: str = ticker

    def get_data(self) -> pd.DataFrame:
        """
        Get data from Yahoo Finance API

        :return: data from Yahoo Finance API
        """

        data = yf.Ticker(self.ticker)
        data = data.history(period="max")
        print("Data from Yahoo Finance API downloaded successfully")
        self.data = data  # save data to class variable
        return data


class SQLrepo:

    def __init__(self, connection):
        self.connection = connection

    def insert_table(self, table_name, records):
        """
        Insert records into a table
        Args:
            table_name: name of the table to insert records
            records: records to insert into the table --> pandas dataframe from yahoo finance
        Returns:
            dict: dictionary with the following keys:
                - records_inserted: True if records were inserted, False otherwise
                - records_count: number of records inserted
        """
        n_inserted = records.to_sql(
            table_name, self.connection, if_exists='replace')
        print(f"Data inserted into {table_name} successfully")

        return {
            "records_inserted": True,
            "records_count": n_inserted,
        }

    def read_table(self, table_name, limit=None):
        """Read table from database
        Parameters
        ----------
        table_name : str
            Name of the table to read
        limit : int, optional 
            Number of records to read. The default is None. --> if None read all records !! just added to test the code

        Returns
        ----------
        pd.DataFrame
            Pandas DataFrame with the records read
            index: DatetimeIndex "Date" . Column names: "Open", "High", "Low", "Close", "Volume", "Dividends", "Stock Splits"
        """
        # create sql Query

        if limit is not None:
            query = f"SELECT * FROM {table_name} LIMIT {limit}"
        else:
            query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(
            query,
            self.connection,
            parse_dates=["Date"],
            index_col=["Date"]
        )

        return df
