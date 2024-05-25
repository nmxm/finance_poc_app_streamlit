import yfinance as yf
from yahoo_fin import stock_info as si
import streamlit as st
import pandas as pd
import plotly.express as px

# Set Page Title
st.set_page_config(page_title="Historical Context", page_icon=":chart_with_upwards_trend:")

# Add a header above the first title with a font size of 36px
st.markdown("<h1 style='font-size:46px'>Dow Jones Industrial Average: A Data Story | 2023</h1>", unsafe_allow_html=True)

# Brief explanation on the Dow Jones Industry
st.write('The Dow Jones Industrial Average (DJIA) is a renowned stock market index that represents 30 large, publicly-owned U.S. companies. Conceived by Charles Dow in 1896, it stands as one of the oldest and most widely recognized market indicators. The DJIA serves as a valuable benchmark reflecting the health and trends of the U.S. economy.')


# Code for the STOCKS PRICE EVOLUTION
# Add a title and a brief description
st.markdown("<h1 style='font-size:23px'>Evolution of Dow Jones Industrial Average Stocks</h1>", unsafe_allow_html=True)
st.write("""
This line chart represents the evolution of the closing prices for the stocks that are part of the 
Dow Jones Industrial Average index, from 2010 to present.
""")

# Define the Tickers of Dow Jones 30
dow_tickers = si.tickers_dow()

# Define the start date
start_date = '2010-01-01'


# Create an empty DataFrame to store all the data
historical_data_all_tickers = pd.DataFrame()

for ticker in dow_tickers:
    # Get the historical stock price data from the start date to present
    stock_data = yf.Ticker(ticker)
    historical_data = stock_data.history(start=start_date)['Close']

    # Add the historical data to the all_data DataFrame
    historical_data_all_tickers[ticker] = historical_data

# Convert the DataFrame to long format for Plotly
long_format_data = historical_data_all_tickers.reset_index().melt('Date', var_name='Ticker', value_name='Stock_Price')

# Create a multiselect box for the user to select which stocks to display
selected_tickers = st.multiselect('Select the tickers you want to display', dow_tickers, default=dow_tickers)

# Filter the data based on the selected tickers
filtered_data = long_format_data[long_format_data['Ticker'].isin(selected_tickers)]

# Create a line plot with Plotly
fig = px.line(filtered_data, x='Date', y='Stock_Price', color='Ticker')

# Use Streamlit to display the plot
st.plotly_chart(fig)

# Code for the MARKET CAPS
# Add a title and a brief description
st.markdown("<h1 style='font-size:23px'>Distribution of Market Capitalization in the Dow Jones Industrial Average</h1>", unsafe_allow_html=True)

st.markdown("""This bar chart illustrates the market capitalization of each company within the Dow Jones Industrial Average. 
Each bar represents a company and its height indicates the company's market capitalization. 
This provides insight into the distribution of value among the constituent companies of the index.""")

# Define an empty dictionary to store the market capitalizations
market_caps = {}

# Get market cap for each ticker
for ticker in dow_tickers:
    stock = yf.Ticker(ticker)
    market_cap = stock.info['marketCap']
    market_caps[ticker] = market_cap

# Convert market caps dictionary to a pandas DataFrame
mc_df = pd.DataFrame(list(market_caps.items()), columns=['Ticker', 'Market Cap']).sort_values(by='Market Cap', ascending = False)

# Create a bar plot
fig = px.bar(mc_df, x='Ticker', y='Market Cap')
st.plotly_chart(fig)

# Code for the SECTOR DISTRIBUTION
st.markdown("<h1 style='font-size:23px'>Sector Distribution of Dow Jones Industrial Average</h1>", unsafe_allow_html=True)

st.markdown("""
This graph represents the distribution of sectors among the companies listed in the Dow Jones Industrial Average. 
The Dow Jones Industrial Average, a price-weighted index of 30 large and publicly owned U.S. companies, reflects various sectors of the economy. 
This visualization provides insight into the sectoral diversity of the index, revealing the economic sectors that dominate the DJIA.
""")

# Define an empty dictionary to store the market sectors
dow_sectors = {}

# Get market sector for each ticker
for ticker in dow_tickers:
    try:
        stock = yf.Ticker(ticker)
        sector = stock.info['sector']
        dow_sectors[ticker] = sector
    except KeyError:
        print(f'Sector information not available for {ticker}')
        continue

# Covnert market sectors to a pandas DataFrame
sector_df = pd.DataFrame(list(dow_sectors.items()), columns= ['Ticker', 'Company_Sectors'])

# Create a pie chart
fig = px.pie(sector_df, names= 'Company_Sectors')
st.plotly_chart(fig)