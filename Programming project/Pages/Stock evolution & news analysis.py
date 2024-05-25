import streamlit as st
import pandas as pd
import yfinance as yf
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from textblob import TextBlob
import os
import  yahoo_fin.stock_info as si
import plotly.graph_objects as go

# Get the current working directory
current_dir = os.getcwd()

# Change the working directory
os.chdir("/Users/antoniofonseca/Desktop/Programming project")

# Get the new working directory
new_dir = os.getcwd()
print(new_dir)

# Print the new working directory
print(f"Changed working directory from {current_dir} to {new_dir}")

# Define the Dow tickers
dowTickers =si.tickers_dow()

# Define the Finviz URL
finviz_url = 'https://finviz.com/quote.ashx?t='

# Define a dictionary to store the sentiment scores
sentiment_scores = {}

def get_sentiment(polarity_score):
    if polarity_score > 0.2:
        return "Positive"
    elif polarity_score < 0:
        return "Negative"
    else:
        return "Neutral"


# Scrape the news articles and calculate the sentiment scores for each ticker
for ticker in dowTickers:
    url = finviz_url + ticker

    #print(url)
    #print("\n")
    req = Request(url=url, headers={'user-agent': 'Mozilla/5.0'})
    resp = urlopen(req)
    html = BeautifulSoup(resp, features="lxml")
    news_table = html.find(id='news-table')
    #print(news_table)
    #print("____")
    if news_table is not None:
        news_rows = news_table.findAll('tr')
        sentiments = []
        for row in news_rows:
            title = row.a.text
            sentiment = TextBlob(title).sentiment.polarity
            sentiments.append(sentiment)
        avg_sentiment = sum(sentiments) / len(sentiments)
        sentiment_scores[ticker] = get_sentiment(avg_sentiment)
    else:
        sentiment_scores[ticker] = None

# Convert the sentiment_scores dictionary to a Pandas DataFrame
df_sentiment = pd.DataFrame.from_dict(sentiment_scores, orient='index', columns=['Sentiment'])
print(df_sentiment)

# Define the Streamlit app
st.title('Dow Jones Sentiment Analysis')
st.write('This app shows the sentiment scores and stock prices of the Dow Jones companies based on their recent news articles.')


# Set background color
st.markdown(
    """
    <style>
    body {
        background-color: #f5f5f5;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Set text color
st.markdown(
    """
    <style>
    body {
        color: #000000;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Define the options for chart type and date range
chart_types = ['Line Chart', 'Candlestick Chart']
date_ranges = ['1 Week', '1 Month', '3 Months', '6 Months', '1 Year', '2 Years', '5 Years', 'Max']

# Add a sidebar to the app for chart type and date range selection
chart_type = st.sidebar.selectbox('Select a chart type', chart_types)
date_range = st.sidebar.selectbox('Select a date range', date_ranges)

sentiments = list(df_sentiment['Sentiment'].unique())

selected_sentiments = st.sidebar.multiselect('Select Sentiment', sentiments)

# Add another multiselect widget for ticker selection
selected_tickers = st.sidebar.multiselect('Select Tickers', dowTickers, default=dowTickers)

# Filter the sentiment scores DataFrame based on the selected sentiment(s)
if selected_sentiments:
    df_sentiment_filtered = df_sentiment[df_sentiment['Sentiment'].isin(selected_sentiments)]
else:
    df_sentiment_filtered = df_sentiment

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


# Loop through the tickers and generate a chart for each ticker
for ticker in selected_tickers:
    # Filter the sentiment scores DataFrame based on the selected sentiment(s)
    if selected_sentiments:
        df_sentiment_filtered = df_sentiment[df_sentiment['Sentiment'].isin(selected_sentiments)]
    else:
        df_sentiment_filtered = df_sentiment

    # Check if the selected ticker is in the filtered sentiment scores DataFrame
    if ticker in df_sentiment_filtered.index:
        # Get the stock data for the selected ticker and date range
        df_stock = get_stock_data(ticker, date_range)

        # Merge the sentiment scores DataFrame and the stock data DataFrame
        df_merged = pd.merge(df_sentiment_filtered, df_stock, how='outer', left_index=True, right_index=True)

        # Plot the selected chart type
        if chart_type == 'Line Chart':
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_merged.index, y=df_merged['Close'], name='Closing Price'))
            fig.update_layout(title=f'{ticker} Stock Price ({date_range})', xaxis_title='Date', yaxis_title='Price')
            st.write(f"Sentiment Score for {ticker}: {df_sentiment.loc[ticker, 'Sentiment']}")
            st.plotly_chart(fig)
        else:
            fig = go.Figure(data=[go.Candlestick(x=df_merged.index, open=df_merged["Open"], 
                        high=df_merged["High"], low=df_merged["Low"], close=df_merged['Close'])])
            fig.update_layout(title=f'{ticker} Candlestick Chart ({date_range})', xaxis_title='Date', yaxis_title='Price')
            st.write(f"Sentiment Score for {ticker}: {df_sentiment.loc[ticker, 'Sentiment']}")
            st.plotly_chart(fig)

# Abrir o cmd e correr o seguinte: python -m streamlit run "C:\Users\franc\Desktop\PythonProject\Projeto_Programming.py"
# python -m streamlit run "C:\Users\franc\Desktop\Programming project\Projeto_Programming.py