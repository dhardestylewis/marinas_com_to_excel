import requests
import json
import time

# Your API key
api_key = "2s4bf7hUMna5NLRGK33o"

# Base URL for Marinas.com API
base_url = "https://api.marinas.com/v1/"

# Function to get the marina by specific coordinates
def get_marina_by_coords(api_key, lat, lon, radius=1, retries=3):
    url = f"{base_url}marinas/search"
    params = {
        "location[lat]": lat,  # Latitude for the marina location
        "location[lon]": lon,  # Longitude for the marina location
        "radius": radius,  # Small radius to target the specific marina
        "access_token": api_key
    }
    attempt = 0
    while attempt < retries:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            print(f"Error: {response.status_code}")
            print("Response content:", response.content)
            attempt += 1
            time.sleep(2)  # wait before retrying
    return None

# Function to get the details of a marina by its ID
def get_marina_details(marina_id, api_key, retries=3):
    url = f"{base_url}marinas/{marina_id}"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    attempt = 0
    while attempt < retries:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            print("Response content:", response.content)
            attempt += 1
            time.sleep(2)  # wait before retrying
    return None

# Specific coordinates for Joseph J. Saladino Memorial Marina at TOBAY
lat = 40.616019  # Converted from 40° 36' 57.67''
lon = -73.425903  # Converted from -73° 25' 33.25''

# Get the list of marinas near the specific location
marinas_list = get_marina_by_coords(api_key, lat, lon)

# Retrieve and print details for the targeted marina
if marinas_list:
    for marina in marinas_list:
        marina_id = marina["id"]
        marina_lat = marina["location"]["lat"]
        marina_lon = marina["location"]["lon"]
        
        # Print basic information
        print(f"Marina ID: {marina_id}")
        print(f"Latitude: {marina_lat}")
        print(f"Longitude: {marina_lon}")
        
        # Get and print detailed information
        marina_details = get_marina_details(marina_id, api_key)
        if marina_details:
            print(json.dumps(marina_details, indent=4))
        print("\n")
else:
    print("Failed to retrieve marinas list after multiple attempts.")

