import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import yfinance as yf
import yahoo_fin.stock_info as si
from statsmodels.tsa.holtwinters import ExponentialSmoothing



def get_stock_price_forecast(stock_symbol, forecast_horizon):
    # Get the last close price
    last_close = yf.Ticker(stock_symbol).history(period="1d").iloc[-1]["Close"]

    # Define the time frame for forecasting
    forecast_start = pd.to_datetime("today") + pd.DateOffset(days=1)

    # Calculate the forecast length based on the forecast horizon
    if forecast_horizon == "1 month":
        forecast_length = 30
    elif forecast_horizon == "3 months":
        forecast_length = 90
    elif forecast_horizon == "6 months":
        forecast_length = 180
    else:  # 1 year
        forecast_length = 365

    # Get historical stock prices using yfinance
    stock_data = yf.download(stock_symbol, start=None)
    stock_df = pd.DataFrame(stock_data)


    # Convert the data to a Pandas DataFrame
    df = pd.DataFrame(stock_df["Close"])
    df.dropna(inplace=True)

    # Apply Holt-Winters method for forecasting
    seasonal_periods = 4  # Adjust the number of seasonal periods as needed
    model = ExponentialSmoothing(df["Close"], trend="add", seasonal="add", seasonal_periods=seasonal_periods)
    forecast = model.fit().forecast(forecast_length)
    forecast_index = pd.date_range(start=df.index[-1] + pd.DateOffset(days=1), periods=forecast_length, freq="D")
    forecast.index = forecast_index

    return df, forecast

def calculate_recommendation(actual_price, forecasted_price):
    if actual_price > forecasted_price:
        return "Sell"
    else:
        return "Buy or Hold"

def main():
    st.title("Stock Price Forecasting App")

    # Define the Dow tickers
    dowTickers = si.tickers_dow()
    ticker = st.selectbox('Select a ticker', dowTickers, index=0)
    forecast_horizon = st.selectbox("Select forecast horizon:", ["1 month", "3 months", "6 months", "1 year"])

    if st.button("Forecast"):
        if not ticker:
            st.error("Please enter a stock symbol.")
        else:
            st.info("Fetching data and performing forecast...")

            # Get the forecasted prices
            df, forecast = get_stock_price_forecast(ticker, forecast_horizon)

            # Plot the original data and the forecasted values
            plt.figure(figsize=(10, 6))
            plt.plot(df.index, df["Close"], label="Actual")
            plt.plot(forecast.index, forecast, label="Forecast")
            plt.xlabel("Date")
            plt.ylabel("Price")
            plt.title(f"Stock Price Forecast for {ticker}")
            plt.legend()
            st.pyplot(plt)

            # Get the most recent stock price
            most_recent_price = df.iloc[-1]["Close"]

            # Get the last value of the forecasted prices
            forecasted_price = forecast.iloc[-1]

            # Calculate recommendation and percentage change
            recommendation = calculate_recommendation(most_recent_price, forecasted_price)
            percentage_change = (forecasted_price - most_recent_price) / most_recent_price * 100

            st.subheader("Forecast Results")
            st.write(f"Recommendation: {recommendation}")
            st.write(f"Percentage Change: {percentage_change:.2f}%")

# Define the Streamlit app
st.set_page_config(page_title="Forecasting Module")


if __name__ == "__main__":
    main()
#%%
get_stock_price_forecast('AAPL', '1 month')