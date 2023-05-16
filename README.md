# Stock prediction ML App

This is a simple stock prediction app that uses machine learning to predict the price of a stock. The app is built using streamlit and uses the yfinance library to get the stock data. The App uses a Auto Regressive Integrated Moving Average (ARIMA) model to predict the price of the stock. The app also plots the data and the predicted price of the stock.

## How to run the app

1. Clone the repository
2. Install the requirements using `pip install -r requirements.txt`
3. Run the app using `streamlit run Deploy.py`

## Demo

    the app is deployed on Streamlit sharing and can be accessed using the link below
<!-- https://mohamedabdelgni-fastdata-deploy-xnkwsa.streamlit.app/ -->

## Data

    the data is collected using the yfinance library and is stored in sqlite database stocks.sqlite

## Models

    the models are active learning models that are trained on the data collected from yfinance every day
    and stored its predictions in the database under the table for every stock with the name of the stock + _pred

## Soon

the app will be deployed on heroku and will be updated with more features and models-->

1. Adding Trading Strategies to the app.
2. Adding more models to the app.
3. Adding more historical data to the app.