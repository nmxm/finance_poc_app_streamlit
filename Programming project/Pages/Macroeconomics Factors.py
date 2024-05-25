import fredapi as fa
import requests
import streamlit as st
import matplotlib.pyplot as plt

# Assign Fred API Key
fred = fa.Fred(api_key='4688605907da3b846bb110da3d8586c3')

# Set Page Title
st.set_page_config(page_title="Marcroeconomic Factors", page_icon=":chart_with_upwards_trend:")

# Add a header above the first title with a font size of 36px
st.markdown("<h1 style='font-size:46px'>Macroeconomic Factors | 2023</h1>", unsafe_allow_html=True)

#Add a brief discussion
st.write('📈 This page provides a comprehensive analysis of the major macroeconomic trends that have a significant impact on the Dow Jones Industrial Average (Dow 30) stock prices.')

# Create a dictionary of macroeconomic factors and their FRED series IDs
factors = {
    'GDP': 'GDP',
    'Interest Rates': 'DGS10',
    'Inflation': 'CPIAUCSL',
    'Unemployment Rate': 'UNRATE',
    'Consumer Confidence': 'UMCSENT'
}

# Create the dropdown menu in Streamlit
selected_factor = st.selectbox('Select a macroeconomic factor', list(factors.keys()))

# Get the FRED series ID for the selected factor
series_id = factors[selected_factor]

# Retrieve the data from the FRED API
data = fred.get_series(series_id, observation_start='2000-01-01')

# Plot the data
plt.plot(data.index, data.values)
plt.title(f'{selected_factor} since 2000')
plt.xlabel('Year')

# Set the ylabel based on the selected factor
if selected_factor == 'GDP':
    plt.ylabel('GDP (Billions of dollars)')
elif selected_factor == 'Interest Rates':
    plt.ylabel('Interest Rates (Percentage)')
elif selected_factor == 'Inflation':
    plt.ylabel('Consumer Price Index')
elif selected_factor == 'Unemployment Rate':
    plt.ylabel('Unemployment Rate (Percentage)')
elif selected_factor == 'Consumer Confidence':
    plt.ylabel('Consumer Confidence Index')

# Customize the plot appearance
plt.xticks(rotation=45)
plt.grid()

# Show the plot in the Streamlit app
st.pyplot(plt.gcf())

# Add a header above the first title with a font size of 36px
st.markdown("<h1 style='font-size:23px'> Macroeconomic Marvels: Stay Up-to-Date on the Latest Economic News!</h1>", unsafe_allow_html=True)

# Get News API URL
news_api_key = 'd78a2f8060f24746a5a7c0d874dd85cd'
news_api_url = "https://newsapi.org/v2/everything"

# Define the query parameters
query_params = {
    "q": "macroeconomics",
    "apiKey": news_api_key,
    "language": "en",
    "pageSize": 10,
    "page": 1,
}

# Make the API request
response = requests.get(news_api_url, params=query_params)

# Check if the request was successful
if response.status_code == 200:
    news_data = response.json()

    # Print the news articles
    for article in news_data["articles"]:
        st.write(article["title"])
        st.write(article["description"])
        if article['urlToImage']:
            st.image(article['urlToImage'], use_column_width=True)
        st.write(f"Published at: {article['publishedAt']}")
        st.write(f"Source: {article['source']['name']}")
        st.write(f"Read more: {article['url']}")
        st.write("---")
else:
    st.write(f"Error: {response.status_code}")

