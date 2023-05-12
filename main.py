from getdata import YahooFinance
from getdata import SQLrepo
import sqlite3
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt
import plotly.express as px
import time

from arch import arch_model


db_name = "stocks.sqlite"

connection=sqlite3.connect(database=db_name,check_same_thread=False)

repo=SQLrepo(connection=connection)


ls_tick={
    "Apple":"AAPL",
    "IBM":"IBM",
    "Microsoft":"MSFT",
    "Google":"GOOG",
    "Tesla":"TSLA",
    "Amazon":"AMZN",
    "META":"META",
}

flag = True
start_time = time.time() 
while flag:
    for key, val in ls_tick.items():
        table_name = key
        tick = val
        data = YahooFinance(tick)
        print(f"Trying Downloading data for {table_name} from Yahoo Finance API")
        data.get_data()
        if len(data.data) <10:
            print(f"Data for {table_name} not available try again")
            #time.sleep(60) 
            break
        else:
            print(f"Data for {table_name} downloaded successfully")
            repo.insert_table(table_name=table_name,records=data.data)
            
        #time.sleep(60) #sleep for 60 seconds
    else:
        print(f"All data downloaded successfully for all stocks and stored in sqlite \ntables {ls_tick.keys()}")
        flag = False

end_time = time.time()  # Record the end time
execution_time = end_time - start_time  # Calculate the execution time in seconds
print(f"Total execution time: {execution_time} seconds")



