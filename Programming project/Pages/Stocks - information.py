import streamlit as st
import os
import pandas as pd
import yfinance as yf
import yahoo_fin.stock_info as si
import plotly.express as px


# Get the current working directory
current_dir = os.getcwd()

# Change the working directory
os.chdir("/Users/antoniofonseca/Desktop/Programming project")

# Get the new working directory
new_dir = os.getcwd()

st.set_page_config(page_title="Stocks Information")

st.title ("Stocks Information")

# Define the Dow tickers
dowTickers = si.tickers_dow()
tickers = st.multiselect('Select one or more tickers', dowTickers, default=["AAPL","KO"])

company_data = []
for ticker in tickers:
    company_info = yf.Ticker(ticker).info
    company_data.append({
    'Ticker': ticker,
    'Company': company_info.get('longName', 'N/A'),
    'Sector': company_info.get('sector', 'N/A'),
    'Industry': company_info.get('industry', 'N/A'),
    'Website': company_info.get('website', 'N/A'),
    'Market Cap': company_info.get('marketCap', 'N/A'),
    'Dividend Yield': company_info.get('dividendYield', 0)
})


# Create a scatter plot with Market Cap on y axis and Dividend Yield on x axis
company_df = pd.DataFrame(company_data, columns=['Company', 'Industry', 'Dividend Yield', 'Market Cap'])

# Create a scatter plot with Market Cap on y axis and Dividend Yield on x axis
fig = px.scatter(company_df, x='Dividend Yield', y='Market Cap', color='Industry', hover_name='Company')

# Set the size and title of the plot
fig.update_layout(width=800, height=600, title='Market Cap vs Dividend Yield')

# Show the plot
st.plotly_chart(fig)

for company in company_data:
    st.markdown(f"**Company Name:** {company['Company']}")
    st.write(f"Industry: {company['Industry']}")
    st.write(f"Sector: {company['Sector']}")
    st.write(f"Market Cap: {company['Market Cap']}")
    st.write(f"Dividend Yield: {round(company['Dividend Yield'],2)}")
    st.write("_________________________________________ ")


#python -m streamlit run "C:\Users\franc\Desktop\Programming project\Homepage.py"