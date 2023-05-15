import streamlit as st

import sqlite3

import pandas as pd

import time

from getdata import SQLrepo

from model_s import StockModel

import plotly.express as px

import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)

connection = sqlite3.connect("stocks.sqlite", check_same_thread=False)
repo = SQLrepo(connection=connection)

st.set_page_config(page_title="Stocks App",
                   page_icon=":moneybag:", layout="wide")

st.markdown(f"<h2 style='text-align: center; '>Stock Returns Prediction ML App</h2>",
            unsafe_allow_html=True)
st.markdown(f"<h4 style='text-align: center; '>Daily Updating Our Models and Data</h4>",
            unsafe_allow_html=True)

ls_tick = {
    "Apple": "AAPL",
    "IBM": "IBM",
    "Microsoft": "MSFT",
    "Google": "GOOG",
    "Tesla": "TSLA",
    "Amazon": "AMZN",
    "META": "META",
}

select_stock = st.selectbox("Stock Selection ", [x for x in ls_tick.keys()])



selection = select_stock
if selection == "none":
    st.error("Please select a stock" , icon="🔥")
    
    
else:

    st.markdown(
        f"<h2 style='text-align: center; '>You selected {select_stock} stock</h2>", unsafe_allow_html=True)
    
    
col1, col2, col3 = st.columns(3)

with col2:
    center_button = st.button('Go', use_container_width=True)
    data_flag = False
    
    if center_button:
        # make animation
        
        print(f"Button clicked  {selection}")
        with col2:
            with st.spinner(''):
                try:
                    data_prices = repo.read_table(table_name=selection)
                    st.success("Data loaded successfully", icon="⚡")
                    data_pred = repo.read_table(table_name=f"{selection}_pred")
                    data_flag = True
                    # show prices data on px graph
                    
                    
                            
                except Exception as e :
                    
                    st.error("Please select a stock",icon="🔥")
                    data_flag = False
                    
                    
                    
def trend(pred, date, pred_str):
    """
    Custom function to show trend.
    
    Args:
        pred (float): Prediction value as a float.
        date (str): String date.
        pred_str (str): String prediction value.
    """
    if pred >= 0.005:
        return st.success(f'Prediction: {pred_str} ✅💯 Verified Up Trend on {date}')
    elif pred >= 0:
        return st.warning(f'Prediction: {pred_str}🟡 Unconfirmed Up Trend on {date}')
    else:
        return st.warning(f'Prediction: {pred_str}🔴 Down Trend on {date}')
    
                    
                    



if data_flag and center_button :
    
    col1, col2, col3 = st.columns(3)
    with col1:
        
        fig = px.line(data_prices, x=data_prices.Date, y="Close", title="Close Price")
        st.plotly_chart(fig)
    col1, col2, col3 = st.columns(3)
    
    with col2:
        next_pred_int_1, next_pred_int_2 = float(data_pred['y_pred'].iat[-2] * 100),float(data_pred['y_pred'].iat[-1] * 100)
        next_pred_str_1, next_pred_str_2= str(round(next_pred_int_1 , 5)) + "%",str(round(next_pred_int_2, 5)) + "%"
        last_pred_date_1,last_pred_date_2  = str(data_pred['index'].iat[-2])[:10],str(data_pred['index'].iat[-1])[:10]
if data_flag and center_button :       
    st.markdown(f"<h4 style='text-align: center; '>Predictions For {select_stock} Stock〽️ </h4>",unsafe_allow_html=True)
    
    trend(pred=next_pred_int_1,date=last_pred_date_1,pred_str=next_pred_str_1)
    trend(pred=next_pred_int_2,date=last_pred_date_2,pred_str=next_pred_str_2)
    
    
    

# footer and Social Media Links

st.markdown(" ")

st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")


st.markdown(f"<h5 style='text-align: center; '>Find me on <a href='https://www.linkedin.com/in/mohamedahmed878/'>LinkedIn</a></h5>",unsafe_allow_html=True)
st.markdown(f"<h6 style='text-align: center; '>📧 Mail me at: mohamed.a.abdelgani@gmail.com </h6>",unsafe_allow_html=True)
st.markdown(f"<h6 style='text-align: center; '>📞 Whatsapp me : +201098557840 </h6>",unsafe_allow_html=True)

st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(f"<h6 style='text-align: center; '>⚠️ This not a financial advice it's just a Scientific Computing  using Machine Learning ⚠️</h6>",unsafe_allow_html=True)

st.markdown(f"<h6 style='text-align: center; '>⚠️ It did a good job in Back testing ⚠️</h6>",unsafe_allow_html=True)


