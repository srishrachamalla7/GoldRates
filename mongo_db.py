# import streamlit as st
# import requests
# import pandas as pd
# import pymongo
# import datetime
# from pymongo import MongoClient
# import matplotlib.pyplot as plt

# # Connect to MongoDB
# client = MongoClient('mongodb+srv://srishnotebooks:JbpvGNb7FWNLVRFJ@goldrates.vx9zl.mongodb.net/?retryWrites=true&w=majority&appName=Goldrates')
# db = client.GoldRates
# collection = db['GoldRates']

# # Backend functions
# def jina(url):
#     base_url = "https://r.jina.ai/"
#     url = base_url + url
#     response = requests.get(url)
#     return response.text

# def price_cities(url):
#     text = jina(url)
#     pos1 = text.find('**')
#     new = text[:pos1]

#     twentytwok = new[int(new.find('22K')):int(new.find('24K'))]
#     value_22k = twentytwok[int(twentytwok.find('\n\n') + 1): int(twentytwok.find('\n\n+'))][3:]
#     value_22k = value_22k.split('\n')[0]

#     twentyfourk = new[int(new.find('24K')):int(new.find('18K'))]
#     value_24k = twentyfourk[int(twentyfourk.find('\n\n') + 1): int(twentyfourk.find('\n\n+'))][3:]
#     value_24k = value_24k.split('\n')[0]

#     eighteenk = new[int(new.find('18K')):]
#     value_18k = eighteenk[int(eighteenk.find('\n\n') + 1): int(eighteenk.find('\n\n+'))][3:]
#     value_18k = value_18k.split('\n')[0]

#     return value_24k, value_22k, value_18k

# # Helper function to insert data only once after 12:30 PM
# def insert_data_if_not_exists(city, date, value_24k, value_22k, value_18k):
#     time_now = datetime.datetime.now()
#     cutoff_time = time_now.replace(hour=12, minute=30, second=0, microsecond=0)
#     query = {"Date": date, "Place": city}
#     if time_now > cutoff_time and not collection.find_one(query):
#         document = {
#             "Date": date,
#             "Place": city,
#             "GoldRate_24k": float(value_24k.replace(',', '')),
#             "GoldRate_22k": float(value_22k.replace(',', '')),
#             "GoldRate_18k": float(value_18k.replace(',', ''))
#         }
#         collection.insert_one(document)
#         st.success(f"Gold rates for {city} on {date} after 12:30 PM have been saved to MongoDB.")

# # Function to fetch weekly data for chart
# def fetch_weekly_data(city):
#     today = datetime.datetime.today()
#     start_date = today - datetime.timedelta(days=7)
#     query = {"Place": city, "Date": {"$gte": start_date.strftime("%Y-%m-%d")}}
#     return list(collection.find(query).sort("Date", -1))

# # List of cities
# cities = ['Ahmedabad', 'Ayodhya', 'Bangalore', 'Bhubaneswar', 'Chandigarh', 'Chennai',
#           'Coimbatore', 'Delhi', 'Hyderabad', 'Jaipur', 'Kerala', 'Kolkata', 'Lucknow',
#           'Madurai', 'Mangalore', 'Mumbai', 'Mysore', 'Nagpur', 'Nashik', 'Patna',
#           'Pune', 'Rajkot', 'Salem', 'Surat', 'Trichy', 'Vadodara', 'Vijayawada', 'Visakhapatnam']

# # Main UI
# st.title('Gold Rates in Indian Cities')
# st.subheader('Select a city to view the current gold rates and a weekly trend.')

# # Dropdown for city selection
# selected_city = st.selectbox('Select a City', cities)

# # Fetch and display gold rates
# if selected_city:
#     date_today = datetime.datetime.today().strftime("%Y-%m-%d")
#     city_url = f"https://www.goodreturns.in/gold-rates/{selected_city}.html"

#     # Try fetching and saving today's data if it doesn't already exist
#     try:
#         value_24k, value_22k, value_18k = price_cities(city_url)
#         insert_data_if_not_exists(selected_city, date_today, value_24k, value_22k, value_18k)

#         # Prepare data for current rates
#         current_data = {
#             'Gold Purity': ['24K', '22K', '18K'],
#             '1g Price (₹)': [float(value_24k.replace(',', '')), float(value_22k.replace(',', '')), float(value_18k.replace(',', ''))],
#             '8g Price (₹)': [float(value_24k.replace(',', '')) * 8, float(value_22k.replace(',', '')) * 8, float(value_18k.replace(',', '')) * 8],
#             '10g Price (₹)': [float(value_24k.replace(',', '')) * 10, float(value_22k.replace(',', '')) * 10, float(value_18k.replace(',', '')) * 10]
#         }

#         # Display current data
#         df = pd.DataFrame(current_data)
#         st.write(f"Gold rates in {selected_city} as of {date_today}:")
#         st.dataframe(df.style.format(precision=2).set_properties(**{
#             'background-color': 'black',
#             'color': 'white',
#             'border-color': 'gray'
#         }))

#         # Weekly trend data
#         weekly_data = fetch_weekly_data(selected_city)
#         if weekly_data:
#             dates = [doc["Date"] for doc in weekly_data]
#             rates_24k = [doc["GoldRate_24k"] for doc in weekly_data]
#             rates_22k = [doc["GoldRate_22k"] for doc in weekly_data]
#             rates_18k = [doc["GoldRate_18k"] for doc in weekly_data]

#             # Plot weekly trends
#             plt.figure(figsize=(10, 5))
#             plt.plot(dates, rates_24k, label="24K Gold", color="gold", marker='o')
#             plt.plot(dates, rates_22k, label="22K Gold", color="orange", marker='o')
#             plt.plot(dates, rates_18k, label="18K Gold", color="brown", marker='o')
#             plt.title(f"Gold Rates Trend in {selected_city} (Past Week)")
#             plt.xlabel("Date")
#             plt.ylabel("Price (₹)")
#             plt.legend()
#             plt.xticks(rotation=45)
#             st.pyplot(plt)

#     except Exception as e:
#         st.error(f"Could not fetch the gold rates. Please try again. {e}")
    
#     # Footer
#     st.markdown("<br><hr><center><p style='color: grey;'>© 2024 All Rights Reserved</p></center><br>", unsafe_allow_html=True)

# import streamlit as st
# import requests
# import pandas as pd
# import pymongo
# import datetime
# from pymongo import MongoClient
# import matplotlib.pyplot as plt

# # Connect to MongoDB
# client = MongoClient('mongodb+srv://srishnotebooks:JbpvGNb7FWNLVRFJ@goldrates.vx9zl.mongodb.net/?retryWrites=true&w=majority&appName=Goldrates')
# db = client.GoldRates
# collection = db['GoldRates']

# # Backend functions
# def jina(url):
#     base_url = "https://r.jina.ai/"
#     url = base_url + url
#     response = requests.get(url)
#     return response.text

# def price_cities(url):
#     text = jina(url)
#     pos1 = text.find('**')
#     new = text[:pos1]

#     twentytwok = new[int(new.find('22K')):int(new.find('24K'))]
#     value_22k = twentytwok[int(twentytwok.find('\n\n') + 1): int(twentytwok.find('\n\n+'))][3:]
#     value_22k = value_22k.split('\n')[0]

#     twentyfourk = new[int(new.find('24K')):int(new.find('18K'))]
#     value_24k = twentyfourk[int(twentyfourk.find('\n\n') + 1): int(twentyfourk.find('\n\n+'))][3:]
#     value_24k = value_24k.split('\n')[0]

#     eighteenk = new[int(new.find('18K')):]
#     value_18k = eighteenk[int(eighteenk.find('\n\n') + 1): int(eighteenk.find('\n\n+'))][3:]
#     value_18k = value_18k.split('\n')[0]

#     return value_24k, value_22k, value_18k

# # Helper function to insert data only once per day (no time constraint)
# def insert_data_if_not_exists(city, date, value_24k, value_22k, value_18k):
#     query = {"Date": date, "Place": city}
#     if not collection.find_one(query):
#         document = {
#             "Date": date,
#             "Place": city,
#             "GoldRate_24k": float(value_24k.replace(',', '')),
#             "GoldRate_22k": float(value_22k.replace(',', '')),
#             "GoldRate_18k": float(value_18k.replace(',', ''))
#         }
#         collection.insert_one(document)
#         st.success(f"Gold rates for {city} on {date} have been saved to MongoDB.")

# # Function to fetch weekly data for chart
# def fetch_weekly_data(city):
#     today = datetime.datetime.today()
#     start_date = today - datetime.timedelta(days=7)
#     query = {"Place": city, "Date": {"$gte": start_date.strftime("%Y-%m-%d")}}
#     return list(collection.find(query).sort("Date", -1))

# # List of cities
# cities = ['Hyderabad', 'Ahmedabad', 'Ayodhya', 'Bangalore', 'Bhubaneswar', 'Chandigarh', 'Chennai',
#           'Coimbatore', 'Delhi',  'Jaipur', 'Kerala', 'Kolkata', 'Lucknow',
#           'Madurai', 'Mangalore', 'Mumbai', 'Mysore', 'Nagpur', 'Nashik', 'Patna',
#           'Pune', 'Rajkot', 'Salem', 'Surat', 'Trichy', 'Vadodara', 'Vijayawada', 'Visakhapatnam']

# # Main UI
# st.title('Gold Rates in Indian Cities')
# st.subheader('Select a city to view the current gold rates and a weekly trend.')
# # Sidebar content
# st.sidebar.title("About the Project")
# # st.sidebar.write("This project, developed by [Srish Rachamalla](https://www.linkedin.com/in/srishrachamalla/) "
# #                  "and [Sai Teja Pallerla](https://www.linkedin.com/in/saiteja-pallerla-668734225/), "
# #                  "fetches and displays the latest gold rates for different cities in India. "
# #                  "You can view rates for 1g, 8g, and 10g for 22K, 24K, and 18K gold.")

# # st.sidebar.write("Use the dropdown to select a city and view the gold rates accordingly.")
# # Sidebar with project and developer info
# # st.sidebar.title("Project Info")
# st.sidebar.write("This project fetches current gold rates for 24K, 22K, and 18K gold from GoodReturns for 28 Indian states. The rates for 1g, 8g, and 10g are displayed.")
# st.sidebar.write("**Developed by:**")
# st.sidebar.write("[Srish Rachamalla](https://www.linkedin.com/in/srishrachamalla/)")
# st.sidebar.write("[Sai Teja Pallerla](https://www.linkedin.com/in/saiteja-pallerla-668734225/)")

# # Dropdown for city selection
# selected_city = st.selectbox('Select a City', cities)

# # Fetch and display gold rates
# if selected_city:
#     date_today = datetime.datetime.today().strftime("%Y-%m-%d")
#     city_url = f"https://www.goodreturns.in/gold-rates/{selected_city}.html"

#     # Try fetching and saving today's data if it doesn't already exist
#     try:
#         value_24k, value_22k, value_18k = price_cities(city_url)
#         insert_data_if_not_exists(selected_city, date_today, value_24k, value_22k, value_18k)

#         # Prepare data for current rates
#         current_data = {
#             'Gold Purity': ['24K', '22K', '18K'],
#             '1g Price (₹)': [float(value_24k.replace(',', '')), float(value_22k.replace(',', '')), float(value_18k.replace(',', ''))],
#             '8g Price (₹)': [float(value_24k.replace(',', '')) * 8, float(value_22k.replace(',', '')) * 8, float(value_18k.replace(',', '')) * 8],
#             '10g Price (₹)': [float(value_24k.replace(',', '')) * 10, float(value_22k.replace(',', '')) * 10, float(value_18k.replace(',', '')) * 10]
#         }

#         # Display current data
#         df = pd.DataFrame(current_data)
#         st.write(f"Gold rates in {selected_city} as of {date_today}:")
#         st.dataframe(df.style.format(precision=2).set_properties(**{
#             'background-color': 'black',
#             'color': 'white',
#             'border-color': 'gray'
#         }))

#         # Weekly trend data
#         weekly_data = fetch_weekly_data(selected_city)
#         if weekly_data:
#             dates = [doc["Date"] for doc in weekly_data]
#             rates_24k = [doc["GoldRate_24k"] for doc in weekly_data]
#             rates_22k = [doc["GoldRate_22k"] for doc in weekly_data]
#             rates_18k = [doc["GoldRate_18k"] for doc in weekly_data]

#             # Plot weekly trends
#             plt.figure(figsize=(10, 5))
#             plt.plot(dates, rates_24k, label="24K Gold", color="gold", marker='o')
#             plt.plot(dates, rates_22k, label="22K Gold", color="red", marker='o')
#             plt.plot(dates, rates_18k, label="18K Gold", color="brown", marker='o')
#             plt.title(f"Gold Rates Trend in {selected_city} (Past Week)")
#             plt.xlabel("Date")
#             plt.ylabel("Price (₹)")
#             plt.legend()
#             plt.xticks(rotation=45)
#             st.pyplot(plt)

#     except Exception as e:
#         st.error(f"Could not fetch the gold rates. Please try again. {e}")
    
#     # Footer
#     st.markdown("<br><hr><center><p style='color: grey;'>© 2024 All Rights Reserved</p></center><br>", unsafe_allow_html=True)


#SS$%
# import streamlit as st
# import requests
# import pandas as pd
# import pymongo
# import datetime
# from pymongo import MongoClient
# import matplotlib.pyplot as plt
# import ssl
# # Connect to MongoDB
# # client = MongoClient('mongodb+srv://srishnotebooks:JbpvGNb7FWNLVRFJ@goldrates.vx9zl.mongodb.net/?retryWrites=true&w=majority&appName=Goldrates')
# MONGO_URI = 'mongodb+srv://srishnotebooks:JbpvGNb7FWNLVRFJ@goldrates.vx9zl.mongodb.net/?retryWrites=true&w=majority&appName=Goldrates'
# client = MongoClient(
#     MONGO_URI,
#     ssl=True,
#     ssl_cert_reqs=ssl.CERT_NONE  # Bypass SSL certificate verification
# )
# db = client.GoldRates
# collection = db['GoldRates']

# # Backend functions
# def jina(url):
#     base_url = "https://r.jina.ai/"
#     url = base_url + url
#     response = requests.get(url)
#     return response.text

# def price_cities(url):
#     text = jina(url)
#     pos1 = text.find('**')
#     new = text[:pos1]

#     twentytwok = new[int(new.find('22K')):int(new.find('24K'))]
#     value_22k = twentytwok[int(twentytwok.find('\n\n') + 1): int(twentytwok.find('\n\n+'))][3:]
#     value_22k = value_22k.split('\n')[0]

#     twentyfourk = new[int(new.find('24K')):int(new.find('18K'))]
#     value_24k = twentyfourk[int(twentyfourk.find('\n\n') + 1): int(twentyfourk.find('\n\n+'))][3:]
#     value_24k = value_24k.split('\n')[0]

#     eighteenk = new[int(new.find('18K')):]
#     value_18k = eighteenk[int(eighteenk.find('\n\n') + 1): int(eighteenk.find('\n\n+'))][3:]
#     value_18k = value_18k.split('\n')[0]

#     return value_24k, value_22k, value_18k

# # Helper function to insert data only once per day (no time constraint)
# def insert_data_if_not_exists(city, date, value_24k, value_22k, value_18k):
#     query = {"Date": date, "Place": city}
#     if not collection.find_one(query):
#         document = {
#             "Date": date,
#             "Place": city,
#             "GoldRate_24k": float(value_24k.replace(',', '')),
#             "GoldRate_22k": float(value_22k.replace(',', '')),
#             "GoldRate_18k": float(value_18k.replace(',', ''))
#         }
#         collection.insert_one(document)
#         # st.success(f"Gold rates for {city} on {date} have been saved to MongoDB.")

# # Function to fetch weekly data for chart
# def fetch_weekly_data(city):
#     today = datetime.datetime.today()
#     start_date = today - datetime.timedelta(days=7)
#     query = {"Place": city, "Date": {"$gte": start_date.strftime("%Y-%m-%d")}}
#     return list(collection.find(query).sort("Date", -1))

# # Function to check if it's the first run of the day after 12:30 PM
# def is_first_run_after_1230():
#     today = datetime.datetime.today()
#     time_check = today.replace(hour=12, minute=30, second=0, microsecond=0)
#     date_check = today.strftime("%Y-%m-%d")
#     return today >= time_check and not collection.find_one({"Date": date_check})

# # Fetch and save rates for all cities
# def fetch_and_save_all_cities():
#     date_today = datetime.datetime.today().strftime("%Y-%m-%d")
#     for city in cities:
#         city_url = f"https://www.goodreturns.in/gold-rates/{city}.html"
#         try:
#             value_24k, value_22k, value_18k = price_cities(city_url)
#             insert_data_if_not_exists(city, date_today, value_24k, value_22k, value_18k)
#         except Exception as e:
#             st.error(f"Could not fetch the gold rates for {city}. {e}")

# # List of cities
# cities = ['Hyderabad', 'Ahmedabad', 'Ayodhya', 'Bangalore', 'Bhubaneswar', 'Chandigarh', 'Chennai',
#           'Coimbatore', 'Delhi',  'Jaipur', 'Kerala', 'Kolkata', 'Lucknow',
#           'Madurai', 'Mangalore', 'Mumbai', 'Mysore', 'Nagpur', 'Nashik', 'Patna',
#           'Pune', 'Rajkot', 'Salem', 'Surat', 'Trichy', 'Vadodara', 'Vijayawada', 'Visakhapatnam']

# # Main UI
# st.title('Gold Rates in Indian Cities')
# st.subheader('Select a city to view the current gold rates and a weekly trend.')
# st.sidebar.title("About the Project")
# st.sidebar.write("This project fetches current gold rates for 24K, 22K, and 18K gold from GoodReturns for 28 Indian states. The rates for 1g, 8g, and 10g are displayed.")
# st.sidebar.write("**Developed by:**")
# st.sidebar.write("[Srish Rachamalla](https://www.linkedin.com/in/srishrachamalla/)")
# st.sidebar.write("[Sai Teja Pallerla](https://www.linkedin.com/in/saiteja-pallerla-668734225/)")

# # Dropdown for city selection
# selected_city = st.selectbox('Select a City', cities)

# # Generate button
# if st.button("Generate Gold Rates"):
#     # If it's the first time after 12:30 PM, fetch and save rates for all cities
#     if is_first_run_after_1230():
#         fetch_and_save_all_cities()
#         st.success("Gold rates for all cities have been fetched and saved.")

#     # Fetch and display gold rates for the selected city
#     if selected_city:
#         date_today = datetime.datetime.today().strftime("%Y-%m-%d")
#         city_url = f"https://www.goodreturns.in/gold-rates/{selected_city}.html"

#         try:
#             value_24k, value_22k, value_18k = price_cities(city_url)
#             insert_data_if_not_exists(selected_city, date_today, value_24k, value_22k, value_18k)

#             # Prepare data for current rates
#             current_data = {
#                 'Gold Purity': ['24K', '22K', '18K'],
#                 '1g Price (₹)': [float(value_24k.replace(',', '')), float(value_22k.replace(',', '')), float(value_18k.replace(',', ''))],
#                 '8g Price (₹)': [float(value_24k.replace(',', '')) * 8, float(value_22k.replace(',', '')) * 8, float(value_18k.replace(',', '')) * 8],
#                 '10g Price (₹)': [float(value_24k.replace(',', '')) * 10, float(value_22k.replace(',', '')) * 10, float(value_18k.replace(',', '')) * 10]
#             }

#             # Display current data
#             df = pd.DataFrame(current_data)
#             st.write(f"Gold rates in {selected_city} as of {date_today}:")
#             st.dataframe(df.style.format(precision=2).set_properties(**{
#                 'background-color': 'black',
#                 'color': 'white',
#                 'border-color': 'gray'
#             }))

#             # Weekly trend data
#             weekly_data = fetch_weekly_data(selected_city)
#             if weekly_data:
#                 dates = [doc["Date"] for doc in weekly_data]
#                 rates_24k = [doc["GoldRate_24k"] for doc in weekly_data]
#                 rates_22k = [doc["GoldRate_22k"] for doc in weekly_data]
#                 rates_18k = [doc["GoldRate_18k"] for doc in weekly_data]

#                 # Plot weekly trends
#                 plt.figure(figsize=(10, 5))
#                 plt.plot(dates, rates_24k, label="24K Gold", color="gold", marker='o')
#                 plt.plot(dates, rates_22k, label="22K Gold", color="red", marker='o')
#                 plt.plot(dates, rates_18k, label="18K Gold", color="brown", marker='o')
#                 plt.title(f"Gold Rates Trend in {selected_city} (Past Week)")
#                 plt.xlabel("Date")
#                 plt.ylabel("Price (₹)")
#                 plt.legend()
#                 plt.xticks(rotation=45)
#                 st.pyplot(plt)

#         except Exception as e:
#             st.error(f"Could not fetch the gold rates. Please try again. {e}")

#     # Footer
#     st.markdown("<br><hr><center><p style='color: grey;'>© 2024 All Rights Reserved</p></center><br>", unsafe_allow_html=True)


import streamlit as st
import requests
import pandas as pd
import pymongo
import datetime
import pytz  # Importing pytz for timezone handling
from pymongo import MongoClient
import matplotlib.pyplot as plt
import ssl
import plotly.graph_objs as go
from plotly.subplots import make_subplots


# Setting up IST timezone
ist_timezone = pytz.timezone("Asia/Kolkata")

# Connect to MongoDB
MONGO_URI = 'mongodb+srv://srishnotebooks:JbpvGNb7FWNLVRFJ@goldrates.vx9zl.mongodb.net/?retryWrites=true&w=majority&appName=Goldrates'
client = MongoClient(
    MONGO_URI,
    ssl=True,
    ssl_cert_reqs=ssl.CERT_NONE  # Bypass SSL certificate verification
)
db = client.GoldRates
collection = db['GoldRates']

# Backend functions
def jina(url):
    base_url = "https://r.jina.ai/"
    url = base_url + url
    response = requests.get(url)
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

# Helper function to insert data only once per day (no time constraint)
def insert_data_if_not_exists(city, date, value_24k, value_22k, value_18k):
    query = {"Date": date, "Place": city}
    if not collection.find_one(query):
        document = {
            "Date": date,
            "Place": city,
            "GoldRate_24k": float(value_24k.replace(',', '')),
            "GoldRate_22k": float(value_22k.replace(',', '')),
            "GoldRate_18k": float(value_18k.replace(',', ''))
        }
        collection.insert_one(document)

# Function to fetch weekly data for chart
def fetch_weekly_data(city):
    today = datetime.datetime.now(ist_timezone)
    start_date = today - datetime.timedelta(days=7)
    query = {"Place": city, "Date": {"$gte": start_date.strftime("%Y-%m-%d")}}
    return list(collection.find(query).sort("Date", -1))

# Function to check if it's the first run of the day after 12:30 PM IST
def is_first_run_after_1230():
    today = datetime.datetime.now(ist_timezone)
    time_check = today.replace(hour=12, minute=30, second=0, microsecond=0)
    date_check = today.strftime("%Y-%m-%d")
    return today >= time_check and not collection.find_one({"Date": date_check})

# Fetch and save rates for all cities
def fetch_and_save_all_cities():
    date_today = datetime.datetime.now(ist_timezone).strftime("%Y-%m-%d")
    for city in cities:
        city_url = f"https://www.goodreturns.in/gold-rates/{city}.html"
        try:
            value_24k, value_22k, value_18k = price_cities(city_url)
            insert_data_if_not_exists(city, date_today, value_24k, value_22k, value_18k)
        except Exception as e:
            st.error(f"Could not fetch the gold rates for {city}. {e}")

# List of cities
cities = ['Hyderabad', 'Ahmedabad', 'Ayodhya', 'Bangalore', 'Bhubaneswar', 'Chandigarh', 'Chennai',
          'Coimbatore', 'Delhi',  'Jaipur', 'Kerala', 'Kolkata', 'Lucknow',
          'Madurai', 'Mangalore', 'Mumbai', 'Mysore', 'Nagpur', 'Nashik', 'Patna',
          'Pune', 'Rajkot', 'Salem', 'Surat', 'Trichy', 'Vadodara', 'Vijayawada', 'Visakhapatnam']

# # Main UI
# st.title('Gold Rates in Indian Cities')
# st.subheader('Select a city to view the current gold rates and a weekly trend.')
# st.sidebar.title("About the Project")
# st.sidebar.write("This project fetches current gold rates for 24K, 22K, and 18K gold from GoodReturns for 28 Indian states. The rates for 1g, 8g, and 10g are displayed.")
# st.sidebar.write("**Developed by:**")
# st.sidebar.write("[Srish Rachamalla](https://www.linkedin.com/in/srishrachamalla/)")
# st.sidebar.write("[Sai Teja Pallerla](https://www.linkedin.com/in/saiteja-pallerla-668734225/)")

# # Dropdown for city selection
# selected_city = st.selectbox('Select a City', cities)

# # Generate button
# if st.button("Generate Gold Rates"):
#     # If it's the first time after 12:30 PM, fetch and save rates for all cities
#     if is_first_run_after_1230():
#         fetch_and_save_all_cities()
#         st.success("Gold rates for all cities have been fetched and saved.")

#     # Fetch and display gold rates for the selected city
#     if selected_city:
#         date_today = datetime.datetime.now(ist_timezone).strftime("%Y-%m-%d")
#         city_url = f"https://www.goodreturns.in/gold-rates/{selected_city}.html"

#         try:
#             value_24k, value_22k, value_18k = price_cities(city_url)
#             insert_data_if_not_exists(selected_city, date_today, value_24k, value_22k, value_18k)

#             # Prepare data for current rates
#             current_data = {
#                 'Gold Purity': ['24K', '22K', '18K'],
#                 '1g Price (₹)': [float(value_24k.replace(',', '')), float(value_22k.replace(',', '')), float(value_18k.replace(',', ''))],
#                 '8g Price (₹)': [float(value_24k.replace(',', '')) * 8, float(value_22k.replace(',', '')) * 8, float(value_18k.replace(',', '')) * 8],
#                 '10g Price (₹)': [float(value_24k.replace(',', '')) * 10, float(value_22k.replace(',', '')) * 10, float(value_18k.replace(',', '')) * 10]
#             }

#             # Display current data
#             df = pd.DataFrame(current_data)
#             st.write(f"Gold rates in {selected_city} as of {date_today}:")
#             st.dataframe(df.style.format(precision=2).set_properties(**{
#                 'background-color': 'black',
#                 'color': 'white',
#                 'border-color': 'gray'
#             }))

#             # Weekly trend data
#             weekly_data = fetch_weekly_data(selected_city)
#             if weekly_data:
#                 dates = [doc["Date"] for doc in weekly_data]
#                 rates_24k = [doc["GoldRate_24k"] for doc in weekly_data]
#                 rates_22k = [doc["GoldRate_22k"] for doc in weekly_data]
#                 rates_18k = [doc["GoldRate_18k"] for doc in weekly_data]

#                 # Plot weekly trends
#                 plt.figure(figsize=(10, 5))
#                 plt.plot(dates, rates_24k, label="24K Gold", color="gold", marker='o')
#                 plt.plot(dates, rates_22k, label="22K Gold", color="red", marker='o')
#                 plt.plot(dates, rates_18k, label="18K Gold", color="brown", marker='o')
#                 plt.title(f"Gold Rates Trend in {selected_city} (Past Week)")
#                 plt.xlabel("Date")
#                 plt.ylabel("Price (₹)")
#                 plt.legend()
#                 plt.xticks(rotation=45)
#                 st.pyplot(plt)

#         except Exception as e:
#             st.error(f"Could not fetch the gold rates. Please try again. {e}")

#     # Footer
#     st.markdown("<br><hr><center><p style='color: grey;'>© 2024 All Rights Reserved</p></center><br>", unsafe_allow_html=True)
#$%^

# Function to display city gold rates with charts
# def display_city_gold_rates(city):
#     date_today = datetime.datetime.now(ist_timezone).strftime("%Y-%m-%d")
#     doc = collection.find_one({"Date": date_today, "Place": city})

#     if doc:
#         # Prepare data for current rates
#         current_data = {
#             'Gold Purity': ['24K', '22K', '18K'],
#             '1g Price (₹)': [doc["GoldRate_24k"], doc["GoldRate_22k"], doc["GoldRate_18k"]],
#             '8g Price (₹)': [doc["GoldRate_24k"] * 8, doc["GoldRate_22k"] * 8, doc["GoldRate_18k"] * 8],
#             '10g Price (₹)': [doc["GoldRate_24k"] * 10, doc["GoldRate_22k"] * 10, doc["GoldRate_18k"] * 10]
#         }

#         # Display current data
#         df = pd.DataFrame(current_data)
#         st.dataframe(df.style.format(precision=2).set_properties(**{
#             'background-color': 'black',
#             'color': 'white',
#             'border-color': 'gray'
#         }))

#         # Weekly trend data
#         weekly_data = fetch_weekly_data(city)
#         if weekly_data:
#             dates = [doc["Date"] for doc in weekly_data]
#             rates_24k = [doc["GoldRate_24k"] for doc in weekly_data]
#             rates_22k = [doc["GoldRate_22k"] for doc in weekly_data]
#             rates_18k = [doc["GoldRate_18k"] for doc in weekly_data]

#             # Plot weekly trends
#             plt.figure(figsize=(10, 5))
#             plt.plot(dates, rates_24k, label="24K Gold", color="gold", marker='o')
#             plt.plot(dates, rates_22k, label="22K Gold", color="red", marker='o')
#             plt.plot(dates, rates_18k, label="18K Gold", color="brown", marker='o')
#             plt.title(f"Gold Rates Trend in {city} (Past Week)")
#             plt.xlabel("Date")
#             plt.ylabel("Price (₹)")
#             plt.legend()
#             plt.xticks(rotation=45)
#             st.pyplot(plt)
#     else:
#         st.error(f"No data found for {city} on {date_today}")
# # Main UI
# st.title('Gold Rates in Indian Cities')
# st.subheader('Select a city to view the current gold rates and a weekly trend.')
# st.sidebar.title("About the Project")
# st.sidebar.write("This project fetches current gold rates for 24K, 22K, and 18K gold from GoodReturns for 28 Indian states. The rates for 1g, 8g, and 10g are displayed.")
# st.sidebar.write("**Developed by:**")
# st.sidebar.write("[Srish Rachamalla](https://www.linkedin.com/in/srishrachamalla/)")
# st.sidebar.write("[Sai Teja Pallerla](https://www.linkedin.com/in/saiteja-pallerla-668734225/)")

# # Dropdown for city selection
# selected_city = st.selectbox('Select a City', cities)

# # Generate button for selected city
# if st.button("Generate Gold Rates for Selected City"):
#     if is_first_run_after_1230():
#         fetch_and_save_all_cities()
#         st.success("Gold rates for all cities have been fetched and saved.")

#     # Fetch and display gold rates for the selected city
#     if selected_city:
#         display_city_gold_rates(selected_city)

# # Generate All button for all cities
# if st.button("Generate All Gold Rates"):
#     # Loop through each city to check and fetch rates if not already in the DB
#     date_today = datetime.datetime.now(ist_timezone).strftime("%Y-%m-%d")
#     for city in cities:
#         # Check if today's data is already in the DB
#         if not collection.find_one({"Date": date_today, "Place": city}):
#             city_url = f"https://www.goodreturns.in/gold-rates/{city}.html"
#             try:
#                 value_24k, value_22k, value_18k = price_cities(city_url)
#                 insert_data_if_not_exists(city, date_today, value_24k, value_22k, value_18k)
#                 st.success(f"Gold rates for {city} saved successfully.")
#             except Exception as e:
#                 st.error(f"Could not fetch the gold rates for {city}. {e}")

#     # Display a message once all data has been saved
#     st.success("Gold rates for all cities have been fetched and saved.")

#     # Fetch and display data from the database with charts for each city
#     for city in cities:
#         st.subheader(f"Gold Rates in {city} as of {date_today}")
#         display_city_gold_rates(city)

# def get_last_friday():
#     today = datetime.datetime.now(ist_timezone)
#     offset = (today.weekday() - 4) % 7  # Calculate days back to last Friday
#     last_friday = today - datetime.timedelta(days=offset)
#     return last_friday.strftime("%Y-%m-%d")

# def display_city_gold_rates(city):
#     today = datetime.datetime.now(ist_timezone)
#     day_today = today.weekday()  # Monday=0, Sunday=6
    
#     if day_today in [5, 6]:  # Saturday (5) or Sunday (6)
#         date_to_fetch = get_last_friday()
#         st.info("The prices you are seeing are from Friday, as today is a weekend.")
#     else:
#         date_to_fetch = today.strftime("%Y-%m-%d")

#     # Fetch data from the database for the appropriate date
#     doc = collection.find_one({"Date": date_to_fetch, "Place": city})

#     if doc:
#         # Prepare data for current rates
#         current_data = {
#             'Gold Purity': ['24K', '22K', '18K'],
#             '1g Price (₹)': [doc["GoldRate_24k"], doc["GoldRate_22k"], doc["GoldRate_18k"]],
#             '8g Price (₹)': [doc["GoldRate_24k"] * 8, doc["GoldRate_22k"] * 8, doc["GoldRate_18k"] * 8],
#             '10g Price (₹)': [doc["GoldRate_24k"] * 10, doc["GoldRate_22k"] * 10, doc["GoldRate_18k"] * 10]
#         }

#         # Display current data
#         df = pd.DataFrame(current_data)
#         st.dataframe(df.style.format(precision=2).set_properties(**{
#             'background-color': 'black',
#             'color': 'white',
#             'border-color': 'gray'
#         }))

#         # Weekly trend data
#         weekly_data = fetch_weekly_data(city)
#         if weekly_data:
#             dates = [doc["Date"] for doc in weekly_data]
#             rates_24k = [doc["GoldRate_24k"] for doc in weekly_data]
#             rates_22k = [doc["GoldRate_22k"] for doc in weekly_data]
#             rates_18k = [doc["GoldRate_18k"] for doc in weekly_data]

#             # Plot weekly trends
#             plt.figure(figsize=(10, 5))
#             plt.plot(dates, rates_24k, label="24K Gold", color="gold", marker='o')
#             plt.plot(dates, rates_22k, label="22K Gold", color="red", marker='o')
#             plt.plot(dates, rates_18k, label="18K Gold", color="brown", marker='o')
#             plt.title(f"Gold Rates Trend in {city} (Past Week)")
#             plt.xlabel("Date")
#             plt.ylabel("Price (₹)")
#             plt.legend()
#             plt.xticks(rotation=45)
#             st.pyplot(plt)
#     else:
#         st.error(f"No data found for {city} on {date_to_fetch}")

# # Main UI
# st.title('Gold Rates in Indian Cities')
# st.subheader('Select a city to view the current gold rates and a weekly trend.')
# st.sidebar.title("About the Project")
# st.sidebar.write("This project fetches current gold rates for 24K, 22K, and 18K gold from GoodReturns for 28 Indian states. The rates for 1g, 8g, and 10g are displayed.")
# st.sidebar.write("**Developed by:**")
# st.sidebar.write("[Srish Rachamalla](https://www.linkedin.com/in/srishrachamalla/)")
# st.sidebar.write("[Sai Teja Pallerla](https://www.linkedin.com/in/saiteja-pallerla-668734225/)")

# # Dropdown for city selection
# selected_city = st.selectbox('Select a City', cities)

# # Generate button for selected city
# if st.button("Generate Gold Rates for Selected City"):
#     today = datetime.datetime.now(ist_timezone)
#     day_today = today.weekday()
#     if is_first_run_after_1230() and day_today not in [5, 6]:  # Avoid saving if it's Saturday or Sunday
#         fetch_and_save_all_cities()
#         st.success("Gold rates for all cities have been fetched and saved.")

#     # Fetch and display gold rates for the selected city
#     if selected_city:
#         display_city_gold_rates(selected_city)

# # Generate All button for all cities
# if st.button("Generate All Gold Rates"):
#     current_time = datetime.datetime.now(ist_timezone).time()
#     date_today = datetime.datetime.now(ist_timezone).strftime("%Y-%m-%d")
#     day_today = datetime.datetime.now(ist_timezone).weekday()

#     # Check if it's after 1 PM and not a weekend
#     if current_time >= datetime.time(13, 0) and day_today not in [5, 6]:
#         for city in cities:
#             # Check if today's data is already in the DB
#             if not collection.find_one({"Date": date_today, "Place": city}):
#                 city_url = f"https://www.goodreturns.in/gold-rates/{city}.html"
#                 try:
#                     value_24k, value_22k, value_18k = price_cities(city_url)
#                     insert_data_if_not_exists(city, date_today, value_24k, value_22k, value_18k)
#                     st.success(f"Gold rates for {city} saved successfully.")
#                 except Exception as e:
#                     st.error(f"Could not fetch the gold rates for {city}. {e}")

#         # Display a message once all data has been saved
#         st.success("Gold rates for all cities have been fetched and saved.")
#     else:
#         st.warning("Gold rates can only be saved to the database after 1 PM on weekdays.")

#     # Fetch and display data from the database with charts for each city
#     for city in cities:
#         st.subheader(f"Gold Rates in {city} as of {date_today}")
#         display_city_gold_rates(city)
#$%^&
import datetime

def get_last_friday():
    today = datetime.datetime.now(ist_timezone)
    offset = (today.weekday() - 4) % 7  # Calculate days back to last Friday
    last_friday = today - datetime.timedelta(days=offset)
    return last_friday.strftime("%Y-%m-%d")

# def display_city_gold_rates(city):
    today = datetime.datetime.now(ist_timezone)
    day_today = today.weekday()  # Monday=0, Sunday=6

    if day_today in [5, 6]:  # Saturday (5) or Sunday (6)
        date_to_fetch = get_last_friday()
        doc = collection.find_one({"Date": date_to_fetch, "Place": city})

        if not doc:
            # If Friday's data is missing, fetch today's data and save it to DB
            date_to_fetch = today.strftime("%Y-%m-%d")
            city_url = f"https://www.goodreturns.in/gold-rates/{city}.html"
            try:
                value_24k, value_22k, value_18k = price_cities(city_url)
                insert_data_if_not_exists(city, date_to_fetch, value_24k, value_22k, value_18k)
                st.info("No data found for Friday, displaying today's rates instead.")
            except Exception as e:
                st.error(f"Could not fetch the gold rates for {city} today. {e}")
                return
    else:
        date_to_fetch = today.strftime("%Y-%m-%d")
        doc = collection.find_one({"Date": date_to_fetch, "Place": city})

    # Display data if found
    if doc:
        current_data = {
            'Gold Purity': ['24K', '22K', '18K'],
            '1g Price (₹)': [doc["GoldRate_24k"], doc["GoldRate_22k"], doc["GoldRate_18k"]],
            '8g Price (₹)': [doc["GoldRate_24k"] * 8, doc["GoldRate_22k"] * 8, doc["GoldRate_18k"] * 8],
            '10g Price (₹)': [doc["GoldRate_24k"] * 10, doc["GoldRate_22k"] * 10, doc["GoldRate_18k"] * 10]
        }

        # Display current data
        df = pd.DataFrame(current_data)
        st.dataframe(df.style.format(precision=2).set_properties(**{
            'background-color': 'black',
            'color': 'white',
            'border-color': 'gray'
        }))

        # Weekly trend data
        weekly_data = fetch_weekly_data(city)
        if weekly_data:
            dates = [doc["Date"] for doc in weekly_data]
            rates_24k = [doc["GoldRate_24k"] for doc in weekly_data]
            rates_22k = [doc["GoldRate_22k"] for doc in weekly_data]
            rates_18k = [doc["GoldRate_18k"] for doc in weekly_data]

            # Plot weekly trends
            plt.figure(figsize=(10, 5))
            plt.plot(dates, rates_24k, label="24K Gold", color="gold", marker='o')
            plt.plot(dates, rates_22k, label="22K Gold", color="red", marker='o')
            plt.plot(dates, rates_18k, label="18K Gold", color="brown", marker='o')
            plt.title(f"Gold Rates Trend in {city} (Past Week)")
            plt.xlabel("Date")
            plt.ylabel("Price (₹)")
            plt.legend()
            plt.xticks(rotation=45)
            st.pyplot(plt)
    else:
        st.error(f"No data found for {city} on {date_to_fetch}")
# def display_city_gold_rates(city):
#     today = datetime.datetime.now(ist_timezone)
#     date_to_fetch = today.strftime("%Y-%m-%d")  # Format date for today
    
#     # Attempt to retrieve document for today's date
#     doc = collection.find_one({"Date": date_to_fetch, "Place": city})
    
#     # Debug print to confirm if the document was retrieved
#     if doc:
#         st.write(f"Document found in DB for {city} on {date_to_fetch}: {doc}")
#     else:
#         st.write(f"No document found in DB for {city} on {date_to_fetch}")
    
#     # Check if data for today or fallback to Friday’s data if today’s data isn’t found
#     if doc:
#         # Extract gold rate data
#         current_data = {
#             'Gold Purity': ['24K', '22K', '18K'],
#             '1g Price (₹)': [doc["GoldRate_24k"], doc["GoldRate_22k"], doc["GoldRate_18k"]],
#             '8g Price (₹)': [doc["GoldRate_24k"] * 8, doc["GoldRate_22k"] * 8, doc["GoldRate_18k"] * 8],
#             '10g Price (₹)': [doc["GoldRate_24k"] * 10, doc["GoldRate_22k"] * 10, doc["GoldRate_18k"] * 10]
#         }

#         # Display current data
#         df = pd.DataFrame(current_data)
#         st.dataframe(df.style.format(precision=2).set_properties(**{
#             'background-color': 'black',
#             'color': 'white',
#             'border-color': 'gray'
#         }))

#         # Display the weekly trend if available
#         weekly_data = fetch_weekly_data(city)
#         if weekly_data:
#             dates = [doc["Date"] for doc in weekly_data]
#             rates_24k = [doc["GoldRate_24k"] for doc in weekly_data]
#             rates_22k = [doc["GoldRate_22k"] for doc in weekly_data]
#             rates_18k = [doc["GoldRate_18k"] for doc in weekly_data]

#             # Plot weekly trends
#             plt.figure(figsize=(10, 5))
#             plt.plot(dates, rates_24k, label="24K Gold", color="gold", marker='o')
#             plt.plot(dates, rates_22k, label="22K Gold", color="red", marker='o')
#             plt.plot(dates, rates_18k, label="18K Gold", color="brown", marker='o')
#             plt.title(f"Gold Rates Trend in {city} (Past Week)")
#             plt.xlabel("Date")
#             plt.ylabel("Price (₹)")
#             plt.legend()
#             plt.xticks(rotation=45)
#             st.pyplot(plt)
#     else:
#         # Display a message if no data is found for today
#         st.warning(f"No data found for {city} on {date_to_fetch}. Check if data for today is correctly stored in the DB.")
def display_city_gold_rates(city):
    today = datetime.datetime.now(ist_timezone)
    date_to_fetch = today.strftime("%Y-%m-%d")
    if today.weekday() >= 5:  # Weekend
        st.info("Today is a weekend. Showing last Friday's data.")
    # Attempt to retrieve document for today's date
    doc = collection.find_one({"Date": date_to_fetch, "Place": city})

    if doc:
        # st.write(f"Document found in DB for {city} on {date_to_fetch}: {doc}")
        st.success(f"Document found in DB for {city}")
        
        # Prepare data for current rates
        current_data = {
            'Gold Purity': ['24K', '22K', '18K'],
            '1g Price (₹)': [doc["GoldRate_24k"], doc["GoldRate_22k"], doc["GoldRate_18k"]],
            '8g Price (₹)': [doc["GoldRate_24k"] * 8, doc["GoldRate_22k"] * 8, doc["GoldRate_18k"] * 8],
            '10g Price (₹)': [doc["GoldRate_24k"] * 10, doc["GoldRate_22k"] * 10, doc["GoldRate_18k"] * 10]
        }

        # Display current data as a table
        df = pd.DataFrame(current_data)
        st.dataframe(df.style.format(precision=2).set_properties(**{
            'background-color': 'black',
            'color': 'white',
            'border-color': 'gray'
        }))

        # Weekly trend data
        weekly_data = fetch_weekly_data(city)
        if weekly_data:
            dates = [doc["Date"] for doc in weekly_data]
            rates_24k = [doc["GoldRate_24k"] for doc in weekly_data]
            rates_22k = [doc["GoldRate_22k"] for doc in weekly_data]
            rates_18k = [doc["GoldRate_18k"] for doc in weekly_data]

            # Create an interactive Plotly line chart
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
                title_text=f"Gold Rates Trend in {city} (Past Week)",
                xaxis_title="Date",
                yaxis_title="Price (₹)",
                hovermode="x unified",
                template="plotly_dark"
            )

            # Display the interactive chart in Streamlit
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"No data found for {city} on {date_to_fetch}.")

# Main UI
st.title('Gold Rates in Indian Cities')
st.subheader('Select a city to view the current gold rates and a weekly trend.')
st.sidebar.title("About the Project")
st.sidebar.write("This project fetches current gold rates for 24K, 22K, and 18K gold from GoodReturns for 28 Indian states. The rates for 1g, 8g, and 10g are displayed.")
st.sidebar.write("**Developed by:**")
st.sidebar.write("[Srish Rachamalla](https://www.linkedin.com/in/srishrachamalla/)")
st.sidebar.write("[Sai Teja Pallerla](https://www.linkedin.com/in/saiteja-pallerla-668734225/)")

# Dropdown for city selection
selected_city = st.selectbox('Select a City', cities)

# Generate button for selected city
if st.button("Generate Gold Rates for Selected City"):
    today = datetime.datetime.now(ist_timezone)
    day_today = today.weekday()
    if is_first_run_after_1230() and day_today not in [5, 6]:  # Avoid saving if it's Saturday or Sunday
        fetch_and_save_all_cities()
        st.success("Gold rates for all cities have been fetched and saved.")

    # Fetch and display gold rates for the selected city
    if selected_city:
        display_city_gold_rates(selected_city)

# Generate All button for all cities
if st.button("Generate All Gold Rates"):
    current_time = datetime.datetime.now(ist_timezone).time()
    date_today = datetime.datetime.now(ist_timezone).strftime("%Y-%m-%d")
    day_today = datetime.datetime.now(ist_timezone).weekday()

    # Check if it's after 1 PM and not a weekend
    if current_time >= datetime.time(13, 0) and day_today not in [5, 6]:
        for city in cities:
            # Check if today's data is already in the DB
            if not collection.find_one({"Date": date_today, "Place": city}):
                city_url = f"https://www.goodreturns.in/gold-rates/{city}.html"
                try:
                    value_24k, value_22k, value_18k = price_cities(city_url)
                    insert_data_if_not_exists(city, date_today, value_24k, value_22k, value_18k)
                    st.success(f"Gold rates for {city} saved successfully.")
                except Exception as e:
                    st.error(f"Could not fetch the gold rates for {city}. {e}")

        # Display a message once all data has been saved
        st.success("Gold rates for all cities have been fetched and saved.")
    else:
        st.warning("Gold rates can only be saved to the database after 1 PM on weekdays.")

    # Fetch and display data from the database with charts for each city
    for city in cities:
        st.subheader(f"Gold Rates in {city} as of {date_today}")
        display_city_gold_rates(city)
