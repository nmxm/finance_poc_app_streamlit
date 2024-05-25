import streamlit as st
import altair as alt
from pytrends.request import TrendReq

# Create a pytrends client
pytrends = TrendReq()

# Set the default keyword
default_keyword = 'stock market'

st.title ("Google Queries")

# Define a text input box for the user to enter a keyword
user_input = st.text_input('Enter a keyword to search:', default_keyword)

# Define a slider to adjust the number of related queries displayed
num_queries = st.slider('Number of related queries to display:', min_value=5, max_value=50, value=20)

# Build the payload for the top searches related to the user's keyword in the past 30 days
pytrends.build_payload([user_input], cat=0, timeframe='today 1-m', geo='', gprop='')

# Get the top related queries and store them in a dataframe
related_queries_df = pytrends.related_queries()[user_input]['top'].head(num_queries)

# Create an Altair chart from the related queries
chart = alt.Chart(related_queries_df).mark_bar().encode(
    x='value:Q',
    y=alt.Y('query:N', sort='-x')
)

# Add a title to the chart
chart_title = f"Top {num_queries} Related Queries for '{user_input.capitalize()}'"
st.write(f"## {chart_title}")
st.altair_chart(chart, use_container_width=True)

