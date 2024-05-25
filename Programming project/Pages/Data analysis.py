import streamlit as st
import os
import pandas as pd
import yfinance as yf
import yahoo_fin.stock_info as si
import plotly.graph_objects as go
import numpy as np
from scipy.stats import jarque_bera


# Get the current working directory
current_dir = os.getcwd()

# Change the working directory
os.chdir("/Users/antoniofonseca/Desktop/Programming project")

# Get the new working directory
new_dir = os.getcwd()

st.set_page_config(page_title="Data Analysis")

st.title ("Stock returns - statistics")

# Define the Dow tickers
dowTickers = si.tickers_dow()
tickers = st.multiselect('Select one or more tickers', dowTickers, default="AAPL")

# Create a dropdown menu to select a date range
date_ranges = ['1 Week', '1 Month', '3 Months', '6 Months', '1 Year', '2 Years', '5 Years', 'Max']
date_range = st.selectbox('Select a date range', date_ranges,index=date_ranges.index("1 Year"))

# Define a function to get the stock data for a ticker and date range
def get_stock_data(ticker, date_range):
    stock = yf.Ticker(ticker)
    if date_range == '1 Week':
        df = stock.history(period='1wk')
    elif date_range == '1 Month':
        df = stock.history(period='1mo')
    elif date_range == '3 Months':
        df = stock.history(period='3mo')
    elif date_range == '6 Months':
        df = stock.history(period='6mo')
    elif date_range == '1 Year':
        df = stock.history(period='1y')
    elif date_range == '2 Years':
        df = stock.history(period='2y')
    elif date_range == '5 Years':
        df = stock.history(period='5y')
    else:
        df = stock.history(period='max')
    return df

# Define a function to calculate statistics of the stock returns

def get_stock_stats(df):
    returns = df['Close'].pct_change().dropna()
    mean_return = np.mean(returns)
    std_return = np.std(returns)
    skewness = returns.skew()
    kurtosis = returns.kurtosis()
    jb_test, jb_p_value = jarque_bera(returns)
    return returns, mean_return, std_return, skewness, kurtosis, jb_test, jb_p_value

# Define an empty dataframe to hold the stock data
stock_data = pd.DataFrame()

# Get the stock data for the selected tickers and date range
for ticker in tickers:
    data = get_stock_data(ticker, date_range)
    returns, mean_return, std_return, skewness, kurtosis, jb_test, jb_p_value = get_stock_stats(data)
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=returns, name=ticker))
    fig.update_layout(title=f'{ticker} Returns Histogram ({date_range})', xaxis_title='Returns', yaxis_title='Frequency')
    st.plotly_chart(fig)
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.write(f"{ticker} Mean Return: {mean_return:.2%}")
    with col2:
        st.write(f"{ticker} Std Deviation: {std_return:.2%}")
    with col3:
        st.write(f"{ticker} Skewness: {skewness:.2f}")
    with col4:
        st.write(f"{ticker} Kurtosis: {kurtosis:.2f}")
    with col5:
        st.write(f"{ticker} JB P-value: {jb_p_value:.2f}")
