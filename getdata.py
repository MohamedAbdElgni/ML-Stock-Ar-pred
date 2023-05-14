from typing import Any

import yfinance as yf

import pandas as pd

import sqlite3


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

        >>> data = YahooFinance('AAPL').get_data()
        >>> data.head()

        :return 
            Pandas Data Frame with the following columns:
                - Date
                - Close
        """

        data = yf.Ticker(self.ticker)
        data = data.history(period="max")
        self.data = data['Close']  # save data to class variable
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
        )

        return df

    def delete_table(self, table_name):
        """
        Delete table from database
        Parameters
        ----------
        table_name : str
            Name of the table to delete
        Returns
        ----------
        dict
            Dictionary with the following keys:
                - table_deleted: True if table was deleted, False otherwise
        """
        query = f"DROP TABLE {table_name}"
        self.connection.execute(query)
        print(f"Table {table_name} deleted successfully")
        return {
            "table_deleted": True
        }

    def delete_all_tables(self):
        """
        Delete all tables from the database
        Returns
        -------
        dict
            Dictionary with the following keys:
                - tables_deleted: List of tables that were deleted
        >>> repo.delete_all_tables()
        Returns:
        ----------
            "All tables deleted successfully"
            Dict: {"tables_deleted": tables_deleted}
        """
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        cursor = self.connection.cursor()
        cursor.execute(query)
        tables = cursor.fetchall()

        tables_deleted = []
        for table in tables:
            table_name = table[0]
            query = f"DROP TABLE {table_name}"
            self.connection.execute(query)
            tables_deleted.append(table_name)

        print("All tables deleted successfully")
        return {
            "tables_deleted": tables_deleted
        }

    def get_tabels_names(self):
        """Get the names of all tables in the database
        Returns:
        ----------
        list
            List of tables in the database
        >>> get_tabels_names() Output >>>  ['AAPL']
        """
        query = """SELECT name FROM sqlite_master WHERE type='table'"""

        cursor = self.connection.cursor()

        cursor.execute(query)

        print(cursor.fetchall())
