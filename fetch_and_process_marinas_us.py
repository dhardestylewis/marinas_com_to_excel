import os
import time
import pandas as pd
import json
import subprocess

# Constants
output_dir = 'us_marinas_data'
os.makedirs(output_dir, exist_ok=True)

api_key = '2s4bf7hUMna5NLRGK33o'  # Replace with your actual API key
radius = 50000  # 50 km radius
max_requests_per_minute = 300
delay_between_requests = 60 / max_requests_per_minute

# Define bounding box for the entire US
north, south, east, west = 49.384358, 24.396308, -66.93457, -125.0

# Grid parameters
lat_step = 1.0  # degrees
lon_step = 1.0  # degrees

# Initialize an empty list to store the data
data_list = []

# Function to flatten JSON structure
def flatten_json(json_obj):
    return {
        'id': json_obj.get('id'),
        'name': json_obj.get('name'),
        'kind': json_obj.get('kind'),
        'rating': json_obj.get('rating'),
        'review_count': json_obj.get('review_count'),
        'lat': json_obj['location'].get('lat'),
        'lon': json_obj['location'].get('lon'),
        'what3words': json_obj['location'].get('what3words'),
        'web_url': json_obj.get('web_url'),
        'api_url': json_obj.get('api_url'),
        'icon_url': json_obj.get('icon_url'),
        'has_diesel': json_obj['fuel'].get('has_diesel'),
        'has_propane': json_obj['fuel'].get('has_propane'),
        'has_gas': json_obj['fuel'].get('has_gas'),
        'propane_price': json_obj['fuel'].get('propane_price'),
        'diesel_price': json_obj['fuel'].get('diesel_price'),
        'gas_regular_price': json_obj['fuel'].get('gas_regular_price'),
        'gas_super_price': json_obj['fuel'].get('gas_super_price'),
        'gas_premium_price': json_obj['fuel'].get('gas_premium_price'),
    }

# Generate grid points
grid_points = []
lat = north
while lat > south:
    lon = west
    while lon < east:
        grid_points.append((lat, lon))
        lon += lon_step
    lat -= lat_step

# Function to fetch data using curl and process it
def fetch_and_process_data(lat, lon, radius, api_key, index):
    command = f'curl -G "https://api.marinas.com/v1/points/search" -d "location[lat]={lat}" -d "location[lon]={lon}" -d "radius={radius}" -d "access_token={api_key}"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        try:
            json_content = json.loads(result.stdout)
            flattened_data = [flatten_json(entry) for entry in json_content.get('data', [])]
            return flattened_data
        except json.JSONDecodeError:
            print(f"Error decoding JSON for region {index}")
    else:
        print(f"Error fetching data for region {index}: {result.stderr}")
    return []

# Fetch data for each grid point and append to data list
for index, (lat, lon) in enumerate(grid_points):
    data = fetch_and_process_data(lat, lon, radius, api_key, index)
    if data:
        data_list.extend(data)
    time.sleep(delay_between_requests)

# Convert the list of data to a DataFrame
df = pd.DataFrame(data_list)

# Save the DataFrame to an Excel file
df.to_excel('us_marinas_data.xlsx', index=False)

print("Data has been saved to us_marinas_data.xlsx")

