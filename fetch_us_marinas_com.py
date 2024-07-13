import os
import time

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

def generate_curl_command(lat, lon, radius, api_key, index):
    return f'curl -G "https://api.marinas.com/v1/points/search" -d "location[lat]={lat}" -d "location[lon]={lon}" -d "radius={radius}" -d "access_token={api_key}" -o "{output_dir}/marinas_{index}.json"'

# Generate grid points
grid_points = []
lat = north
while lat > south:
    lon = west
    while lon < east:
        grid_points.append((lat, lon))
        lon += lon_step
    lat -= lat_step

# Generate and execute curl commands
for index, (lat, lon) in enumerate(grid_points):
    command = generate_curl_command(lat, lon, radius, api_key, index)
    print(f"Executing: {command}")
    os.system(command)
    time.sleep(delay_between_requests)

print("Finished fetching all marina data.")

