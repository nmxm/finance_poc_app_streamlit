import yfinance as yf
import datetime
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import streamlit as st
import plotly.graph_objs as go
import yahoo_fin.stock_info as si

# Define function to get stock return data
def get_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)['Close']
    return stock_data

#Split the data set into train and test
def lstm_split(data, n_steps):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)
    X, y = [],[]
    for i in range(n_steps,len(data)):
        X.append(scaled_data[i-n_steps:i,0])
        y.append(scaled_data[i,0])
    return np.array(X), np.array(y)

#create the lstm model
def lstm_model(x_train, y_train, units=50, epochs=5, n_steps=20):
    x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))
    # create and fit the LSTM network
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1],1)))
    model.add(LSTM(units=50))
    model.add(Dense(1))

    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(x_train, y_train, epochs=epochs, batch_size=1, verbose=2)
    
    return model

#predict the return based on the trained model
def predict_return(model, dataset, valid_set, n_steps=20):
    
    #predicting len(valid_set) values, using past n_steps from the train data
    inputs = dataset[len(dataset)-len(valid_set)-n_steps:].values
    inputs = inputs.reshape(-1,1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    inputs = scaler.fit_transform(inputs)

    X_test = []
    for i in range(n_steps,inputs.shape[0]):
        X_test.append(inputs[i-n_steps:i,0])
    X_test = np.array(X_test)

    X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))
    closing_price = model.predict(X_test)
    closing_price = scaler.inverse_transform(closing_price)
    
    return closing_price

# Set up the Streamlit app
st.set_page_config(page_title="Return Forecasting")
st.title("Forecasts")

dowTickers = si.tickers_dow()

# Define the options for chart type and date range
chart_types = ['Line Chart']

selected_tickers = st.sidebar.multiselect('Select Tickers', dowTickers, default=dowTickers[0])

# Set default start and end dates
start_date = datetime.date(2020, 1, 1)
end_date = datetime.date.today()

# Allow user to select start and end dates
start_date_ = st.sidebar.date_input('Start Date', value=start_date, max_value=end_date)
end_date_ = st.sidebar.date_input('End Date', value=end_date, min_value=start_date, max_value=end_date)

# Allow user to select forecast period
forecast_period = st.sidebar.slider('Forecast Period (days)', min_value=1, max_value=360, value=5)

# Show date range on sidebar
st.sidebar.write("Data from " + start_date.strftime("%Y-%m-%d") + " to " + end_date.strftime("%Y-%m-%d"))

# Loop over each ticker and plot its historical returns and predictions
for ticker in selected_tickers:
    stock_data = pd.DataFrame(get_stock_data(ticker, start_date, end_date), columns=["Close"])

    X1, y1 = lstm_split(stock_data.values, n_steps = 20)
    model = lstm_model(X1, y1, units=50, epochs=2, n_steps=20)
    forecast_index = pd.date_range(start=end_date, periods=forecast_period, freq='D')
    closing_price = predict_return(model, stock_data, forecast_index, n_steps=20)

    # Create line chart of historical returns and predictions
    st.subheader(ticker)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], name='Closing Price'))
    fig.update_layout(title=f'{ticker} Stock Price ({forecast_period} days forecast)', xaxis_title='Date', yaxis_title='Price')
    st.plotly_chart(fig)

    # Make predictions and create line chart of predictions
    predit = pd.DataFrame(index=forecast_index, columns=["Predictions"])
    predit["Predictions"] = closing_price
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=predit.index, y=predit["Predictions"], name='Closing Price'))
    st.plotly_chart(fig)

if closing_price[-1] > stock_data['Close'][-1]:
    st.write("The predicted stock price for tomorrow is higher than the last seen value. You may consider buying the stock.")
else:
    st.write("The predicted stock price for tomorrow is not higher than the last seen value. You may consider holding or selling the stock.")

