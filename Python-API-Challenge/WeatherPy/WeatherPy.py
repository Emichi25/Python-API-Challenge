#!/usr/bin/env python
# coding: utf-8

# # WeatherPy
# 
# ---
# 
# ## Starter Code to Generate Random Geographic Coordinates and a List of Cities

# In[1]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
from scipy.stats import linregress

# Import the OpenWeatherMap API key
from api_keys import weather_api_key


# Import citipy to determine the cities based on latitude and longitude
from citipy import citipy


# ### Generate the Cities List by Using the `citipy` Library

# In[2]:


# Empty list for holding the latitude and longitude combinations
lat_lngs = []

# Empty list for holding the cities names
cities = []

# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180)

# Create a set of random lat and lng combinations
lats = np.random.uniform(lat_range[0], lat_range[1], size=1500)
lngs = np.random.uniform(lng_range[0], lng_range[1], size=1500)
lat_lngs = zip(lats, lngs)

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name
    
    # If the city is unique, then add it to a our cities list
    if city not in cities:
        cities.append(city)

# Print the city count to confirm sufficient count
print(f"Number of cities in the list: {len(cities)}")


# ---

# ## Requirement 1: Create Plots to Showcase the Relationship Between Weather Variables and Latitude
# 
# ### Use the OpenWeatherMap API to retrieve weather data from the cities list generated in the started code

# In[3]:


# Set the API base URL
url = "http://api.openweathermap.org/data/2.5/weather?" 
units = "metric"

# Define an empty list to fetch the weather data for each city
city_data = []

# Print to logger
print("Beginning Data Retrieval     ")
print("-----------------------------")

# Create counters
record_count = 1
set_count = 1

# Loop through all the cities in our list to fetch weather data
for i, city in enumerate(cities):
        
    # Group cities in sets of 50 for logging purposes
    if (i % 50 == 0 and i >= 50):
        set_count += 1
        record_count = 0

    # Create endpoint URL with each city
   # city_url = url + "appid=" + weather_api_key + "&q=" + city
   
    city_url = f"{url}appid={weather_api_key}&units={units}&q={city}"
    
   
    
    
    # Log the url, record, and set numbers
    print("Processing Record %s of Set %s | %s" % (record_count, set_count, city))

    # Add 1 to the record count
    record_count += 1

    # Run an API request for each of the cities
    try:
        # Parse the JSON and retrieve data
        city_weather = requests.get(city_url).json()

        # Parse out latitude, longitude, max temp, humidity, cloudiness, wind speed, country, and date
        #https://openweathermap.org/faq#error401 - APIs
        #https://openweathermap.org/current
        city_lat = city_weather["coord"]["lat"]
        city_lng = city_weather["coord"]["lon"]
        city_max_temp = city_weather["main"]["temp_max"]
        city_humidity = city_weather["main"]["humidity"]
        city_clouds = city_weather["clouds"]["all"]
        city_wind = city_weather["wind"]["speed"]
        city_country = city_weather["sys"]["country"]
        city_date = city_weather["dt"]

        # Append the City information into city_data list
        city_data.append({"City": city, 
                          "Lat": city_lat, 
                          "Lng": city_lng, 
                          "Max Temp": city_max_temp,
                          "Humidity": city_humidity,
                          "Cloudiness": city_clouds,
                          "Wind Speed": city_wind,
                          "Country": city_country,
                          "Date": city_date})

    # If an error is experienced, skip the city
    except:
        print("City not found. Skipping...")
        pass
              
# Indicate that Data Loading is complete 
print("-----------------------------")
print("Data Retrieval Complete      ")
print("-----------------------------")


# In[4]:


city_url


# In[5]:


# Convert the cities weather data into a Pandas DataFrame
city_data_df = pd.DataFrame(city_data)

# Show Record Count
city_data_df.count()


# In[6]:


# Display sample data
city_data_df.head(10)


# In[7]:


# Export the City_Data into a csv
city_data_df.to_csv("C:/Users/evanm/OneDrive/Desktop/Python-API-Challenge/output_data/cities.csv", index_label="City_ID")   


# In[8]:


# Read saved data
city_data_df = pd.read_csv("C:/Users/evanm/OneDrive/Desktop/Python-API-Challenge/output_data/cities.csv", index_col="City_ID")

# Display sample data
city_data_df.head()


# ### Create the Scatter Plots Requested
# 
# #### Latitude Vs. Temperature

# In[9]:


# Build scatter plot for latitude vs. temperature
plt.scatter(city_data_df["Lat"], city_data_df["Max Temp"], color = "blue", alpha = 0.5)

# Incorporate the other graph properties
# See 6.1-6.3 notes and lectures
plt.title("City Max Latitude vs. Temperature (2022-10-18)")
plt.ylabel("Max Temperature") 
plt.xlabel("Latitude")
plt.grid(True)

# Save the figure
plt.savefig("C:/Users/evanm/OneDrive/Desktop/Python-API-Challenge/output_data/Fig1.png")

# Show plot
plt.show()


# #### Latitude Vs. Humidity

# In[10]:


# Build the scatter plots for latitude vs. humidity
plt.scatter(city_data_df["Lat"], city_data_df["Humidity"], color = "blue", alpha = 0.5)

# Incorporate the other graph properties
plt.title("City Latitude vs. Humidity (2022-10-18)")
plt.ylabel("Humidity")
plt.xlabel("Latitude")
plt.grid(True)

# Save the figure
plt.savefig("C:/Users/evanm/OneDrive/Desktop/Python-API-Challenge/output_data/Fig2.png")

# Show plot
plt.show()


# #### Latitude Vs. Cloudiness

# In[11]:


# Build the scatter plots for latitude vs. cloudiness
plt.scatter(city_data_df["Lat"], city_data_df["Cloudiness"], color = "blue", alpha = 0.5)

# Incorporate the other graph properties
plt.title("City Latitude vs. Cloudiness (2022-10-18)")
plt.ylabel("Cloudiness")
plt.xlabel("Latitude")
plt.grid(True)

# Save the figure
plt.savefig("C:/Users/evanm/OneDrive/Desktop/Python-API-Challenge/output_data/Fig3.png")

# Show plot
plt.show()


# #### Latitude vs. Wind Speed Plot

# In[12]:


# Build the scatter plots for latitude vs. wind speed
plt.scatter(city_data_df["Lat"], city_data_df["Wind Speed"], color = "blue", alpha = 0.5)

# Incorporate the other graph properties
plt.title("City Latitude vs. Wind Speed (2022-10-18)")
plt.ylabel("Wind Speed")
plt.xlabel("Latitude")
plt.grid(True)

# Save the figure
plt.savefig("C:/Users/evanm/OneDrive/Desktop/Python-API-Challenge/output_data/Fig4.png")

# Show plot
plt.show()


# ---
# 
# ## Requirement 2: Compute Linear Regression for Each Relationship
# 

# In[13]:


# Define a function to create Linear Regression plots


# https://www.mathworks.com/help/matlab/data_analysis/linear-regression.html
# https://python-graph-gallery.com/scatter-plot/
# Look 6.1-6.3 notes, work and review videos
# https://www.geeksforgeeks.org/linear-regression-formula/?ref=gcse
#  https://stackoverflow.com/questions/19068862/how-to-overplot-a-line-on-a-scatter-plot-in-python


def LinearRegression(x_data,y_data,x_lbl,y_lbl,lbl_pos,ifig):
   
    (slope, intercept, rvalue, pvalue, stderr) = linregress(x_data, y_data)
    print(f"The r-squared is: {rvalue}")
    regress_values = x_data * slope + intercept
    equation = "y = " + str(round(slope,2)) + "x + " + str(round(intercept,2))

    plt.scatter(x_data,y_data)
    plt.xlabel(x_lbl)
    plt.ylabel(y_lbl)
    plt.plot(x_data,regress_values,"r-")
    plt.annotate(equation,lbl_pos,fontsize=12,color="red")
 
   
# Get regression values

# Please see below


# In[14]:


# Create a DataFrame with the Northern Hemisphere data (Latitude >= 0)
northern_hemi_df = city_data_df.loc[city_data_df["Lat"] >= 0]


# Display sample data
northern_hemi_df.head()


# In[15]:


# Create a DataFrame with the Southern Hemisphere data (Latitude < 0)
southern_hemi_df = city_data_df.loc[city_data_df["Lat"] < 0]


# Display sample data
southern_hemi_df.head()


# ###  Temperature vs. Latitude Linear Regression Plot

# In[16]:


# Linear regression on Northern Hemisphere
# See 6.1-6.3 notes and lectures
x_lbl = "Lat"
y_lbl = "Max Temp"
plt.title("Northern Hemisphere Latitude vs. Max Temp")
# Fixed position where I think it will populate. Run again to see if it shows up with new data if not present.
lbl_pos = (0,10)
LinearRegression(northern_hemi_df[x_lbl],northern_hemi_df[y_lbl],x_lbl,y_lbl,lbl_pos,5)
plt.grid()

plt.show()


# In[17]:


# Linear regression on Southern Hemisphere

x_lbl = "Lat"
y_lbl = "Max Temp"
plt.title("Southern Hemisphere Latitude vs. Max Temp") 
lbl_pos = (0,10)
LinearRegression(southern_hemi_df[x_lbl],southern_hemi_df[y_lbl],x_lbl,y_lbl,lbl_pos,6)
plt.grid()


plt.show()


# # Examining the present data on 8/9/23
# 
# 
# # Northern Hemisphere:There is a weak correlation between Latitude and Max Temp (coefficient:-0.6500600512632367 )
# 
# 
# # Southern Hemisphere:There is a strong correlation between Latitude and Max Temp (coefficient: 0.795771517576791 )

# ### Humidity vs. Latitude Linear Regression Plot

# In[18]:


# Northern Hemisphere

x_lbl = "Lat"
y_lbl = "Humidity"
plt.title("Northern Hemisphere Latitude vs. Humidity")
lbl_pos = (0,10)
LinearRegression(northern_hemi_df[x_lbl],northern_hemi_df[y_lbl],x_lbl,y_lbl,lbl_pos,7)
plt.grid()


plt.show()


# In[19]:


# Southern Hemisphere



x_lbl = "Lat"
y_lbl = "Humidity"
plt.title("Southern Hemisphere Latitude vs. Humidity")
lbl_pos = (0,10)
LinearRegression(southern_hemi_df[x_lbl],southern_hemi_df[y_lbl],x_lbl,y_lbl,lbl_pos,8)
plt.grid()




plt.show()


# # Examining the present data on 8/9/23
# 
# 
# # Northern Hemisphere: There is a negligible correlation between Latitude and Humidity (coefficient: 0.016297787595760324  )
# 
# 
# # Southern Hemisphere: There is a weak correlation between Latitude and Humidity (coefficient: -0.14002431564571824 )

# ### Cloudiness vs. Latitude Linear Regression Plot

# In[20]:


# Northern Hemisphere
x_lbl = "Lat"
y_lbl = "Cloudiness"
plt.title("Northern Hemisphere Latitude vs. Cloudiness on")
lbl_pos = (0,10)
LinearRegression(northern_hemi_df[x_lbl],northern_hemi_df[y_lbl],x_lbl,y_lbl,lbl_pos,9)
plt.grid()



plt.show()


# In[21]:


# Southern Hemisphere
x_lbl = "Lat"
y_lbl = "Cloudiness"
plt.title("Southern Hemisphere Latitude vs. Cloudiness")
lbl_pos = (0,10)
LinearRegression(southern_hemi_df[x_lbl],southern_hemi_df[y_lbl],x_lbl,y_lbl,lbl_pos,10)
plt.grid()


plt.show()


# # Examining the present data on 8/9/23
# 
# 
# # Northern Hemisphere: There is a weak correlation between Latitude and Cloudiness (coefficient: -0.11162660304353758 )
# 
# 
# # Southern Hemisphere: There is a weak correlation between Latitude and Cloudiness (coefficient: -0.15593197901007388 )

# ### Wind Speed vs. Latitude Linear Regression Plot

# In[22]:


# Northern Hemisphere
x_lbl = "Lat"
y_lbl = "Wind Speed"
plt.title("Northern Hemisphere Latitude vs Wind Speed")
lbl_pos = (0,10)
LinearRegression(northern_hemi_df[x_lbl],northern_hemi_df[y_lbl],x_lbl,y_lbl,lbl_pos,11)
plt.grid()



plt.show()


# In[23]:


# Southern Hemisphere
x_lbl = "Lat"
y_lbl = "Wind Speed"
plt.title("Southern Hemisphere Latitude vs Wind Speed")
lbl_pos = (0,10)
LinearRegression(southern_hemi_df[x_lbl],southern_hemi_df[y_lbl],x_lbl,y_lbl,lbl_pos,12)
plt.grid()


plt.show()


# # Examining the present data on 8/9/23
# 
# 
# # Northern Hemisphere: There is a weak correlation between Latitude and Wind Speed (coefficient: -0.19302767574640908 )
# 
# 
# # Southern Hemisphere: There is a weak correlation between Latitude and Wind Speed (coefficient: -0.13859693701284212 )
