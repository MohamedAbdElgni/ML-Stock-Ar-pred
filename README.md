# Stock Daily Prediction ML App

This is a simple stock prediction app that uses machine learning to predict the price of a stock. The app is built using streamlit and uses the yfinance library to get the stock data. The App uses a Auto Regressive Integrated Moving Average (ARIMA) model to predict the price of the stock. The app also plots the data and the predicted price of the stock.

## How to run the app

1. Clone the repository
2. Install the requirements using `pip install -r requirements.txt`
3. Run the app using `streamlit run Deploy.py`

## Usage

1. Select the stock you want to predict

2. Simply Click Go and the app will predict the price of the stock

## Files

1. Deploy.py: The main file that runs the app
2. stocks.sqlite: The database that stores the data collected from yfinance.
3. models.py: The file that contains the models used in the app and it's a custom class .
4. getdata.py: The file that contains the functions that collect the data from yfinance and stores it in the database.
5. get_data_daily.py: This file uses the getdata.py file to collect the data every day.
6. train_model_daily.py: This file uses the models.py file to train the models every day.
7. backtesting.ipynb: This file contains the back testing of the models.
8. requirements.txt: This file contains the requirements to run the app.
9. .github/workflows/main.yml: This file contains the github actions to run the app every day and collect the data and train the models.

## Demo

    The app is deployed on Streamlit sharing and can be accessed using the link below :- 
    
[App](https://mohamedabdelgni-mlstockarpred-deploy-ho85w7.streamlit.app/).

## Data

    The data is collected using the yfinance library and is stored in sqlite database stocks.sqlite

## Models

    The models are active  that are trained on the data every day
    and stored its predictions in the database under the table for every stock with the name of the stock+_pred
    >>>> Example: if the stock is AAPL the table name will be Apple_pred

## Back testing

    You can find the back testing notebook in backtesting.ipynb

## Soon

    the app will be deployed on a Cloud and will be updated with more features and models-->

1. Adding Trading Strategies to the app.
2. Adding more models to the app.
3. Adding more historical data to the app.
4. Add a grid search to find the best parameters for the model for ever stock.
5. Add a Crypto currency prediction section to the app.
6. Add Hourly and minute data and predictions to the app.

## Contributions

    Feel free to contribute to the app by adding more models or more features to the app.
    under Branch develop

## Author

    Mohamed Abdelghani
