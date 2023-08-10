#!/usr/bin/env python
# coding: utf-8

# # VacationPy
# ---
# 
# ## Starter Code to Import Libraries and Load the Weather and Coordinates Data

# In[1]:


# Dependencies and Setup
import hvplot.pandas
import pandas as pd
import requests
#import geopandas as gpd

# Import API key
from api_keys import geoapify_key


# In[2]:


# Load the CSV file created in Part 1 into a Pandas DataFrame
city_data_df = pd.read_csv("C:/Users/evanm/OneDrive/Desktop/Python-API-Challenge/output_data/cities.csv")



# Display sample data
city_data_df.head(1000)


# ---
# 
# ### Step 1: Create a map that displays a point for every city in the `city_data_df` DataFrame. The size of the point should be the humidity in each city.

# In[3]:


get_ipython().run_cell_magic('capture', '--no-display', '\n# Configure the map plot\n\n# https://hvplot.holoviz.org/user_guide/Geographic_Data.html\n# See 6.1 - 6.3 examples\nmap_plot = city_data_df.hvplot.points(\n                                        "Lng", \n                                        "Lat", \n                                        geo = True, \n                                        size = "Humidity",\n                                        scale = 1,\n                                        color = "City",\n                                        alpha = 0.5,\n                                       # tiles = "ESRI",\n                                        tiles = "OSM",\n                                        frame_width = 650,\n                                        frame_height = 600\n                                        )\n                                    \n                                    \n#maps_plot = city_data_df.hvplot(global_extent=True, frame_height=450, tiles=True)                               \n\n# Display the map\nmap_plot\n')


# ### Step 2: Narrow down the `city_data_df` DataFrame to find your ideal weather condition

# In[4]:


# Narrow down cities that fit criteria and drop any results with null values

# Drop any rows with null values

preferred_cities_df = city_data_df.loc[(city_data_df["Max Temp"] <= 27) 
                                       & (city_data_df["Max Temp"] >= 21)
                                       & (city_data_df["Wind Speed"] <= 4.5) 
                                       & (city_data_df["Cloudiness"] == 0)].dropna()

# Display sample data
preferred_cities_df.head(1000) 


# ### Step 3: Create a new DataFrame called `hotel_df`.

# In[5]:


# Use the Pandas copy function to create DataFrame called hotel_df to store the city, country, coordinates, and humidity
hotel_df = preferred_cities_df[["City","Country", "Lat", "Lng","Humidity"]].copy()

# Add an empty column, "Hotel Name," to the DataFrame so you can store the hotel found using the Geoapify API
hotel_df["Hotel Name"] = ""

# Display sample data
hotel_df


# ### Step 4: For each city, use the Geoapify API to find the first hotel located within 10,000 metres of your coordinates.

# In[6]:


# Set parameters to search for a hotel
# Joseph helped with this on 8/9/23
radius = 10000
params = {   "categories": "accommodation.hotel", 
             "apiKey": geoapify_key,
              "limit": 20
         }

# Print a message to follow up the hotel search
print("Starting hotel search")

# Iterate through the hotel_df DataFrame
for index, row in hotel_df.iterrows():
    # get latitude, longitude from the DataFrame
    latitude =  row["Lat"]
    longitude = row["Lng"]
    
    # Add filter and bias parameters with the current city's latitude and longitude to the params dictionary
    params["filter"] =  f"circle:{longitude},{latitude},{radius}"
  
    params["bias"] = f"proximity:{longitude},{latitude}"
   
    
    # Set base URL
    base_url = "https://api.geoapify.com/v2/places"

    
    # Make and API request using the params dictionaty
    name_address = requests.get(base_url, params = params)

    
    
    # Convert the API response to JSON format
    name_address = name_address.json()
    
    # Grab the first hotel from the results and store the name in the hotel_df DataFrame
    try:
        hotel_df.loc[index, "Hotel Name"] = name_address["features"][0]["properties"]["name"]
    except (KeyError, IndexError):
        # If no hotel is found, set the hotel name as "No hotel found".
        hotel_df.loc[index, "Hotel Name"] = "No hotel found"
        
    # Log the search results
    print(f"{hotel_df.loc[index, 'City']} - nearest hotel: {hotel_df.loc[index, 'Hotel Name']}")

# Display sample data
hotel_df


# ### Step 5: Add the hotel name and the country as additional information in the hover message for each city in the map.

# In[7]:


get_ipython().run_cell_magic('capture', '--no-display', '# https://hvplot.holoviz.org/user_guide/Geographic_Data.html\n# See 6.1 - 6.3 examples\n# Configure the map plot\nmap_plot_hotel = hotel_df.hvplot.points(\n                                        "Lng", \n                                        "Lat", \n                                        geo = True, \n                                        size = "Humidity",\n                                        scale = 1,\n                                        color = "City",\n                                        hover_cols = ["Hotel Name", "Country"],\n                                        alpha = 0.5,\n                                        tiles = "OSM",\n                                        frame_width = 700,\n                                        frame_height = 500\n                                        )\n\n# Display the map\nmap_plot_hotel\n')


# In[ ]:




