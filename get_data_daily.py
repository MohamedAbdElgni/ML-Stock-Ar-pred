from getdata import YahooFinance
from getdata import SQLrepo
import sqlite3
import multiprocessing
import time




db_name = "stocks.sqlite"

connection = sqlite3.connect(database=db_name, check_same_thread=False)

repo = SQLrepo(connection=connection)

#Important to note that the table name should be the same as the ticker name and the values used for the API requests,
#Otherwise the code will not work, and table name is the company global name to make naming easy in the front end .
ls_tick = {
    "Apple": "AAPL",
    "IBM": "IBM",
    "Microsoft": "MSFT",
    "Google": "GOOG",
    "Tesla": "TSLA",
    "Amazon": "AMZN",
    "META": "META",
}

#using multiprocessing to download data for all stocks at the same time for faster execution
def process_stock(ticker, table_name):
    # Add Exception handling -- To be added later
    data = YahooFinance(ticker)
    print(f"Trying Downloading data for {table_name} from Yahoo Finance API")
    data.get_data()
    if len(data.data) < 10:
        print(f"Data for {table_name} not available, try again")
    else:
        print(f"Data for {table_name} downloaded !!!!")
        repo.insert_table(table_name=table_name, records=data.data)


if __name__ == '__main__':
    start_time = time.time()

    processes = []
    for table_name, ticker in ls_tick.items():
        p = multiprocessing.Process(
            target=process_stock, args=(ticker, table_name))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    end_time = time.time()  # Record the end time
    # Calculate the execution time in seconds
    execution_time = end_time - start_time
    print(f"Total execution time: {execution_time} seconds")
