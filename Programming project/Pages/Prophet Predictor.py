import yfinance as yf
import datetime as dt
import streamlit as st
from fbprophet import Prophet
import yahoo_fin.stock_info as si
import matplotlib.pyplot as plt

# Set Page Title
st.set_page_config(page_title="Prophet Predictions", page_icon="🔮")

# Add a header above the first title with a font size of 36px
st.markdown("<h1 style='font-size:46px'>🔮 Prophet Predictions</h1>", unsafe_allow_html=True)

# Define the Tickers of Dow Jones 30
tickers_dow = si.tickers_dow()

# Create the dropdown menu in Streamlit
selected_ticker = st.selectbox('Select a Stock in Dow Jones Industry', tickers_dow)

# Define the time range for historical data
start_date = dt.datetime(2020,1,1)
end_date = dt.datetime.now()

# Get the historical stock price data
stock = yf.Ticker(selected_ticker)
historical_data = stock.history(start=start_date, end=end_date).reset_index()[['Date','Close']]

# Rename the columns to match Prophet's requirements
historical_data.columns = ['ds', 'y']

# Remove timezone from ds
historical_data['ds']=historical_data['ds'].dt.tz_localize(None)

# Set Prophet seasonality
prophet = Prophet(daily_seasonality=True)
prophet.fit(historical_data)

# Generate future dates period
future_dates = prophet.make_future_dataframe(periods=90)
predictions = prophet.predict(future_dates)

# Print the predictions for the stock price
fig=prophet.plot(predictions)

# Edit the labels
plt.xlabel('Date')
plt.ylabel('StockPrice')
plt.title('Stock Prediction')

# Show the plot in st
st.pyplot(fig)