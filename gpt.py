import streamlit as st
import requests
import pandas as pd
import pymongo
import datetime
import pytz
from pymongo import MongoClient
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import ssl

# Setting up IST timezone
ist_timezone = pytz.timezone("Asia/Kolkata")

# Connect to MongoDB
MONGO_URI = 'mongodb+srv://srishnotebooks:JbpvGNb7FWNLVRFJ@goldrates.vx9zl.mongodb.net/?retryWrites=true&w=majority&appName=Goldrates'
# client = MongoClient(MONGO_URI, ssl=True, ssl_cert_reqs=ssl.CERT_NONE)
client = MongoClient(
    MONGO_URI,
    ssl=True,
    ssl_cert_reqs=ssl.CERT_NONE  # Bypass SSL certificate verification
)
db = client.GoldRates
collection = db['GoldRates']
# List of cities
cities = ['Hyderabad', 'Ahmedabad', 'Ayodhya', 'Bangalore', 'Bhubaneswar', 'Chandigarh', 'Chennai',
          'Coimbatore', 'Delhi',  'Jaipur', 'Kerala', 'Kolkata', 'Lucknow',
          'Madurai', 'Mangalore', 'Mumbai', 'Mysore', 'Nagpur', 'Nashik', 'Patna',
          'Pune', 'Rajkot', 'Salem', 'Surat', 'Trichy', 'Vadodara', 'Vijayawada', 'Visakhapatnam']
# Backend functions
def jina(url):
    base_url = "https://r.jina.ai/"
    response = requests.get(base_url + url)
    return response.text
def price_cities(url):
    text = jina(url)
    pos1 = text.find('**')
    new = text[:pos1]

    twentytwok = new[int(new.find('22K')):int(new.find('24K'))]
    value_22k = twentytwok[int(twentytwok.find('\n\n') + 1): int(twentytwok.find('\n\n+'))][3:]
    value_22k = value_22k.split('\n')[0]

    twentyfourk = new[int(new.find('24K')):int(new.find('18K'))]
    value_24k = twentyfourk[int(twentyfourk.find('\n\n') + 1): int(twentyfourk.find('\n\n+'))][3:]
    value_24k = value_24k.split('\n')[0]

    eighteenk = new[int(new.find('18K')):]
    value_18k = eighteenk[int(eighteenk.find('\n\n') + 1): int(eighteenk.find('\n\n+'))][3:]
    value_18k = value_18k.split('\n')[0]

    return value_24k, value_22k, value_18k

def insert_data_if_not_exists(city, date, value_24k, value_22k, value_18k):
    if not collection.find_one({"Date": date, "Place": city}):
        document = {
            "Date": date,
            "Place": city,
            "GoldRate_24k": float(value_24k.replace(',', '')),
            "GoldRate_22k": float(value_22k.replace(',', '')),
            "GoldRate_18k": float(value_18k.replace(',', ''))
        }
        collection.insert_one(document)

def fetch_weekly_data(city):
    today = datetime.datetime.now(ist_timezone)
    start_date = today - datetime.timedelta(days=7)
    return list(collection.find({"Place": city, "Date": {"$gte": start_date.strftime("%Y-%m-%d")}}).sort("Date", -1))

def is_first_run_after_1230():
    today = datetime.datetime.now(ist_timezone)
    time_check = today.replace(hour=12, minute=30, second=0, microsecond=0)
    date_check = today.strftime("%Y-%m-%d")
    return today >= time_check and not collection.find_one({"Date": date_check})

def fetch_and_save_all_cities():
    date_today = datetime.datetime.now(ist_timezone).strftime("%Y-%m-%d")
    for city in cities:
        city_url = f"https://www.goodreturns.in/gold-rates/{city}.html"
        try:
            value_24k, value_22k, value_18k = price_cities(city_url)
            insert_data_if_not_exists(city, date_today, value_24k, value_22k, value_18k)
        except Exception as e:
            st.error(f"Could not fetch the gold rates for {city}. {e}")

# Get last Friday's date
def get_last_friday():
    today = datetime.datetime.now(ist_timezone)
    last_friday = today - datetime.timedelta(days=(today.weekday() - 4) % 7)
    return last_friday.strftime("%Y-%m-%d")
def fetch_historical_data(city, days=365):  # Default to the past year
    end_date = datetime.datetime.now(ist_timezone)
    start_date = end_date - datetime.timedelta(days=days)
    return list(collection.find({"Place": city, "Date": {"$gte": start_date.strftime("%Y-%m-%d"), "$lte": end_date.strftime("%Y-%m-%d")}}).sort("Date", 1))
def display_city_gold_rates(city):
    today = datetime.datetime.now(ist_timezone)
    date_to_fetch = today.strftime("%Y-%m-%d")

    if today.weekday() >= 5:  # Weekend
        st.info("Today is a weekend. Showing last available data.")

    # Attempt to retrieve document for today's date
    doc = collection.find_one({"Date": date_to_fetch, "Place": city})

    if not doc:
        st.warning(f"No data found for {city} on {date_to_fetch}. Scraping for latest data...")
        city_url = f"https://www.goodreturns.in/gold-rates/{city}.html"
        try:
            value_24k, value_22k, value_18k = price_cities(city_url)
            insert_data_if_not_exists(city, date_to_fetch, value_24k, value_22k, value_18k)
            st.success(f"Fetched latest gold rates for {city}.")

            # Prepare current rates table with newly scraped data
            current_data = {
                'Gold Purity': ['24K', '22K', '18K'],
                '1g Price (₹)': [float(value_24k.replace(',', '')), float(value_22k.replace(',', '')), float(value_18k.replace(',', ''))],
                '8g Price (₹)': [float(value_24k.replace(',', '')) * 8, float(value_22k.replace(',', '')) * 8, float(value_18k.replace(',', '')) * 8],
                '10g Price (₹)': [float(value_24k.replace(',', '')) * 10, float(value_22k.replace(',', '')) * 10, float(value_18k.replace(',', '')) * 10]
            }

            # Display current data
            df = pd.DataFrame(current_data)
            # st.dataframe(df)

            # Create a styled dataframe for Streamlit
            styled_df = df.style.format(precision=2).set_properties(**{
                'background-color': 'black',
                'color': 'white',
                'border-color': 'gray',
                'font-size': '16px',
                'text-align': 'center'
            }).set_table_attributes('style="width: 80%; margin: auto;"')  # Center the table

            st.dataframe(styled_df)

            # Fetch historical data
            historical_data = fetch_historical_data(city)
            
            if historical_data:
                dates = [doc["Date"] for doc in historical_data]
                rates_24k = [doc["GoldRate_24k"] for doc in historical_data]
                rates_22k = [doc["GoldRate_22k"] for doc in historical_data]
                rates_18k = [doc["GoldRate_18k"] for doc in historical_data]

                # Create an interactive Plotly line chart for the historical data
                fig = make_subplots(specs=[[{"secondary_y": False}]])

                # Add 24K data trace
                fig.add_trace(
                    go.Scatter(x=dates, y=rates_24k, mode='lines+markers', name="24K Gold",
                            line=dict(color="gold"), marker=dict(size=8)),
                    secondary_y=False,
                )

                # Add 22K data trace
                fig.add_trace(
                    go.Scatter(x=dates, y=rates_22k, mode='lines+markers', name="22K Gold",
                            line=dict(color="red"), marker=dict(size=8)),
                    secondary_y=False,
                )

                # Add 18K data trace
                fig.add_trace(
                    go.Scatter(x=dates, y=rates_18k, mode='lines+markers', name="18K Gold",
                            line=dict(color="brown"), marker=dict(size=8)),
                    secondary_y=False,
                )

                # Set chart titles and layout
                fig.update_layout(
                    title_text=f"Gold Rates Trend in {city} (Historical Data)",
                    xaxis_title="Date",
                    yaxis_title="Price (₹)",
                    hovermode="x unified",
                    template="plotly_dark"
                )

                # Display the interactive chart in Streamlit
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning(f"No historical data found for {city}.")

        except Exception as e:
            st.error(f"Could not fetch the gold rates for {city}. {e}")
            return
    # else:
        # st.success(f"Gold Rates for {city} on {date_to_fetch}")
    # Prepare current rates table
    if doc:
        st.success(f"Gold Rates for {city} on {date_to_fetch}")

        # Prepare data for current rates
        current_data = {
            'Gold Purity': ['24K', '22K', '18K'],
            '1g Price (₹)': [doc["GoldRate_24k"], doc["GoldRate_22k"], doc["GoldRate_18k"]],
            '8g Price (₹)': [doc["GoldRate_24k"] * 8, doc["GoldRate_22k"] * 8, doc["GoldRate_18k"] * 8],
            '10g Price (₹)': [doc["GoldRate_24k"] * 10, doc["GoldRate_22k"] * 10, doc["GoldRate_18k"] * 10]
        }

        # Display current data as a stylish table
        df = pd.DataFrame(current_data)

        # Create a styled dataframe for Streamlit
        styled_df = df.style.format(precision=2).set_properties(**{
            'background-color': 'black',
            'color': 'white',
            'border-color': 'gray',
            'font-size': '16px',
            'text-align': 'center'
        }).set_table_attributes('style="width: 80%; margin: auto;"')  # Center the table

        st.dataframe(styled_df)

        # Fetch historical data
        historical_data = fetch_historical_data(city)
        
        if historical_data:
            dates = [doc["Date"] for doc in historical_data]
            rates_24k = [doc["GoldRate_24k"] for doc in historical_data]
            rates_22k = [doc["GoldRate_22k"] for doc in historical_data]
            rates_18k = [doc["GoldRate_18k"] for doc in historical_data]

            # Create an interactive Plotly line chart for the historical data
            fig = make_subplots(specs=[[{"secondary_y": False}]])

            # Add 24K data trace
            fig.add_trace(
                go.Scatter(x=dates, y=rates_24k, mode='lines+markers', name="24K Gold",
                           line=dict(color="gold"), marker=dict(size=8)),
                secondary_y=False,
            )

            # Add 22K data trace
            fig.add_trace(
                go.Scatter(x=dates, y=rates_22k, mode='lines+markers', name="22K Gold",
                           line=dict(color="red"), marker=dict(size=8)),
                secondary_y=False,
            )

            # Add 18K data trace
            fig.add_trace(
                go.Scatter(x=dates, y=rates_18k, mode='lines+markers', name="18K Gold",
                           line=dict(color="brown"), marker=dict(size=8)),
                secondary_y=False,
            )

            # Set chart titles and layout
            fig.update_layout(
                title_text=f"Gold Rates Trend in {city} (Historical Data)",
                xaxis_title="Date",
                yaxis_title="Price (₹)",
                hovermode="x unified",
                template="plotly_dark"
            )

            # Display the interactive chart in Streamlit
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"No historical data found for {city}.")
    # else:
        # st.warning(f"No data found for {city} on {date_to_fetch}.")
# Main UI
st.title('Gold Rates in Indian Cities')
st.subheader('Select a city to view the current gold rates and a weekly trend.')
st.sidebar.title("About the Project")
st.sidebar.write("This project fetches current gold rates for 24K, 22K, and 18K gold from GoodReturns for 28 Indian states. The rates for 1g, 8g, and 10g are displayed.")
st.sidebar.write("**Developed by:**")
st.sidebar.write("[Srish Rachamalla](https://www.linkedin.com/in/srishrachamalla/)")
st.sidebar.write("[Sai Teja Pallerla](https://www.linkedin.com/in/saiteja-pallerla-668734225/)")

selected_city = st.selectbox('Select a City', cities)

if st.button("Generate Gold Rates for Selected City"):
    if is_first_run_after_1230() and datetime.datetime.now(ist_timezone).weekday() not in [5, 6]: 
        fetch_and_save_all_cities()
        st.success("Gold rates for all cities have been fetched and saved.")
    if selected_city:
        display_city_gold_rates(selected_city)

if st.button("Generate All Gold Rates"):
    current_time = datetime.datetime.now(ist_timezone).time()
    if current_time >= datetime.time(13, 0) and datetime.datetime.now(ist_timezone).weekday() not in [5, 6]:
        for city in cities:
            if not collection.find_one({"Date": datetime.datetime.now(ist_timezone).strftime("%Y-%m-%d"), "Place": city}):
                city_url = f"https://www.goodreturns.in/gold-rates/{city}.html"
                try:
                    value_24k, value_22k, value_18k = price_cities(city_url)
                    insert_data_if_not_exists(city, datetime.datetime.now(ist_timezone).strftime("%Y-%m-%d"), value_24k, value_22k, value_18k)
                    st.success(f"Gold rates for {city} saved successfully.")
                except Exception as e:
                    st.error(f"Could not fetch the gold rates for {city}. {e}")
        st.success("Gold rates for all cities have been fetched and saved.")
    else:
        st.warning("Gold rates can only be saved to the database after 1 PM on weekdays.")
    for city in cities:
        st.subheader(f"Gold Rates in {city} as of {datetime.datetime.now(ist_timezone).strftime('%Y-%m-%d')}")
        display_city_gold_rates(city)
