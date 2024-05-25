import streamlit as st
import os
import yfinance as yf

# Set page configuration
st.set_page_config(page_title="Homepage")

# Ticker symbol for Dow 30 is ^DJI
ticker = "^DJI"

# Get historical data for Dow 30 from January 1, 2023, up to most recent data
dow_data = yf.download(ticker, start="2023-01-01")["Close"]

# Get the current working directory
current_dir = os.getcwd()

# Change the working directory
os.chdir("/Users/antoniofonseca/Desktop/Programming project")

# Get the new working directory
new_dir = os.getcwd()

# Add a header above the first title with a font size of 36px and a custom font
st.markdown("<h1 style='font-size:46px; font-family: Arial, sans-serif;'>Programming for Data Science | 2023</h1>", unsafe_allow_html=True)

st.title("The Profit Predictor: dashboard on stock prediction")

# Add some padding and margin to the top and bottom of the header
st.markdown("<div style='padding-top: 20px; padding-bottom: 20px;'></div>", unsafe_allow_html=True)

st.sidebar.success("Select a page above")

# Add a chart or graph to display stock market trends
st.markdown("<h2 style='text-align:center;'>Market Return Index (Dow 30)</h2>", unsafe_allow_html=True)
st.line_chart(data=dow_data)

# Add introductory text
st.write("""
         Welcome to The Profit Predictor! Our app aims to forecast the future returns of stocks and help you make informed investment decisions. 
         Use the navigation bar on the left to explore different sections of the app and get started with your stock market analysis.
         """)

# Add some color to your page
st.markdown("<style>body {background-color: #F2F2F2;}</style>", unsafe_allow_html=True)

# Add footer
st.write("---")
st.write("By António Fonseca, Celso Cassama, Francisco Loureiro, Nuno Marques")

#python -m streamlit run "C:\Users\franc\Desktop\Programming project\Homepage.py"
#python -m streamlit run "/Users/antoniofonseca/Desktop/Programming project/Homepage.py"
