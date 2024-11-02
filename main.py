# import streamlit as st
# import requests

# # Your backend functions
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

#     twentyfourk = new[int(new.find('24K')):int(new.find('18K'))]
#     value_24k = twentyfourk[int(twentyfourk.find('\n\n') + 1): int(twentyfourk.find('\n\n+'))][3:]

#     eighteenk = new[int(new.find('18K')):]
#     value_18k = eighteenk[int(eighteenk.find('\n\n') + 1): int(eighteenk.find('\n\n+'))][3:]

#     return value_22k, value_24k, value_18k

# # City list
# cities = ['Ahmedabad', 'Ayodhya', 'Bangalore', 'Bhubaneswar', 'Chandigarh', 'Chennai',
#           'Coimbatore', 'Delhi', 'Hyderabad', 'Jaipur', 'Kerala', 'Kolkata', 'Lucknow',
#           'Madurai', 'Mangalore', 'Mumbai', 'Mysore', 'Nagpur', 'Nashik', 'Patna',
#           'Pune', 'Rajkot', 'Salem', 'Surat', 'Trichy', 'Vadodara', 'Vijayawada', 'Visakhapatnam']

# # Streamlit app
# st.title('Gold Rates in Indian States')

# # Dropdown for selecting the city
# selected_city = st.selectbox('Select a City', cities)

# # Fetch and display gold rates when a city is selected
# if selected_city:
#     city_url = f"https://www.goodreturns.in/gold-rates/{selected_city}.html"
    
#     # Fetch the prices using your backend function
#     try:
#         x, y, z = price_cities(city_url)
#         st.write(f"Gold rates in {selected_city}:")
#         st.write(f"22K Gold: ₹{x}")
#         st.write(f"24K Gold: ₹{y}")
#         st.write(f"18K Gold: ₹{z}")
#     except:
#         st.error("Could not fetch the gold rates. Please try again.")
# import streamlit as st
# import requests
# import pandas as pd

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

#     twentyfourk = new[int(new.find('24K')):int(new.find('18K'))]
#     value_24k = twentyfourk[int(twentyfourk.find('\n\n') + 1): int(twentyfourk.find('\n\n+'))][3:]

#     eighteenk = new[int(new.find('18K')):]
#     value_18k = eighteenk[int(eighteenk.find('\n\n') + 1): int(eighteenk.find('\n\n+'))][3:]

#     return float(value_22k.replace(',', '')), float(value_24k.replace(',', '')), float(value_18k.replace(',', ''))

# # City list
# cities = ['Ahmedabad', 'Ayodhya', 'Bangalore', 'Bhubaneswar', 'Chandigarh', 'Chennai',
#           'Coimbatore', 'Delhi', 'Hyderabad', 'Jaipur', 'Kerala', 'Kolkata', 'Lucknow',
#           'Madurai', 'Mangalore', 'Mumbai', 'Mysore', 'Nagpur', 'Nashik', 'Patna',
#           'Pune', 'Rajkot', 'Salem', 'Surat', 'Trichy', 'Vadodara', 'Vijayawada', 'Visakhapatnam']

# # Streamlit UI
# st.set_page_config(page_title="Gold Rates in Indian States", layout="wide")

# # Sidebar with project and developer info
# st.sidebar.title("Project Info")
# st.sidebar.write("This project fetches current gold rates for 24K, 22K, and 18K gold from GoodReturns for 28 Indian states. The rates for 1g, 8g, and 10g are displayed.")
# st.sidebar.write("**Developed by:**")
# st.sidebar.write("[Srish Rachamalla](https://www.linkedin.com/in/srishrachamalla/)")
# st.sidebar.write("[Sai Teja Pallerla](https://www.linkedin.com/in/saiteja-pallerla-668734225/)")

# # Dropdown for selecting a city
# st.title('Gold Rates in Indian States')
# selected_city = st.selectbox('Select a City', cities)

# Fetch and display gold rates when a city is selected
# if selected_city:
#     city_url = f"https://www.goodreturns.in/gold-rates/{selected_city}.html"
    
#     try:
#         # Fetch the gold prices using your backend function
#         price_22k, price_24k, price_18k = price_cities(city_url)
        
#         # Prepare data for table
#         data = {
#             'Karat': ['22K', '24K', '18K'],
#             '1g (₹)': [price_22k, price_24k, price_18k],
#             '8g (₹)': [price_22k * 8, price_24k * 8, price_18k * 8],
#             '10g (₹)': [price_22k * 10, price_24k * 10, price_18k * 10]
#         }
        
#         df = pd.DataFrame(data)
        
#         # Display the table in a styled format
#         st.write(f"### Gold rates in {selected_city}:")
#         st.table(df.style.format({'1g (₹)': '₹{:.2f}', '8g (₹)': '₹{:.2f}', '10g (₹)': '₹{:.2f}'}).background_gradient(cmap='YlOrRd'))
    
#     except Exception as e:
#         st.error(f"Could not fetch the gold rates. Please try again later.{e}")
import streamlit as st
import requests
import pandas as pd

# Your backend functions
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

# List of cities
cities = ['Ahmedabad', 'Ayodhya', 'Bangalore', 'Bhubaneswar', 'Chandigarh', 'Chennai',
          'Coimbatore', 'Delhi', 'Hyderabad', 'Jaipur', 'Kerala', 'Kolkata', 'Lucknow',
          'Madurai', 'Mangalore', 'Mumbai', 'Mysore', 'Nagpur', 'Nashik', 'Patna',
          'Pune', 'Rajkot', 'Salem', 'Surat', 'Trichy', 'Vadodara', 'Vijayawada', 'Visakhapatnam']

# Sidebar content
st.sidebar.title("About the Project")
# st.sidebar.write("This project, developed by [Srish Rachamalla](https://www.linkedin.com/in/srishrachamalla/) "
#                  "and [Sai Teja Pallerla](https://www.linkedin.com/in/saiteja-pallerla-668734225/), "
#                  "fetches and displays the latest gold rates for different cities in India. "
#                  "You can view rates for 1g, 8g, and 10g for 22K, 24K, and 18K gold.")

# st.sidebar.write("Use the dropdown to select a city and view the gold rates accordingly.")
# Sidebar with project and developer info
# st.sidebar.title("Project Info")
st.sidebar.write("This project fetches current gold rates for 24K, 22K, and 18K gold from GoodReturns for 28 Indian states. The rates for 1g, 8g, and 10g are displayed.")
st.sidebar.write("**Developed by:**")
st.sidebar.write("[Srish Rachamalla](https://www.linkedin.com/in/srishrachamalla/)")
st.sidebar.write("[Sai Teja Pallerla](https://www.linkedin.com/in/saiteja-pallerla-668734225/)")

# Main UI
st.title('Gold Rates in Indian Cities')
st.subheader('Select a city to view the current gold rates')

# Dropdown for city selection
selected_city = st.selectbox('Select a City', cities)

# Fetch and display gold rates
if selected_city:
    city_url = f"https://www.goodreturns.in/gold-rates/{selected_city}.html"
    
    # Fetch the prices using your backend function
    try:
        value_24k, value_22k, value_18k = price_cities(city_url)

        # Convert string values to float for calculation
        value_22k = round(float(value_22k.replace(',', '')),2)
        value_24k = round(float(value_24k.replace(',', '')),2)
        value_18k = round(float(value_18k.replace(',', '')),2)

        # Prepare data for table
        data = {
            # 'SNO': [1, 2, 3],
            'Gold Purity': ['24K', '22K', '18K'],
            '1g Price (₹)': [value_24k, value_22k, value_18k],
            '8g Price (₹)': [value_24k * 8, value_22k * 8, value_18k * 8],
            '10g Price (₹)': [value_24k * 10, value_22k * 10, value_18k * 10]
        }

        # Create a DataFrame for display
        df = pd.DataFrame(data,index=[1, 2, 3])

        # Display the DataFrame as a table
        st.write(f"Gold rates in {selected_city}:")
        # st.dataframe(df.style.set_properties(**{
        #     'background-color': 'black',
        #     'color': 'white',
        #     'border-color': 'ash'
        # }))
        st.dataframe(df.style.format(precision=2).set_properties(**{
            'background-color': 'black',
            'color': 'white',
            'border-color': 'ash'
        }))

    except Exception as e:
        st.error(f"Could not fetch the gold rates. Please try again.{e}")
    # except:
    #     st.error("Could not fetch the gold rates. Please try again.")
    st.markdown("<br><hr><center><p style='color: grey;'>© 2024 All Rights Reserved</p></center><br>", unsafe_allow_html=True)


# # Custom CSS to improve UI appearance
# st.markdown("""
#     <style>
#     .stSidebar {
#         background-color: #f4f4f4;
#     }
#     .stApp {
#         background-color: #000000;
#     }
#     </style>
#     """, unsafe_allow_html=True)

