import osmnx as ox
import pandas as pd
import json
import logging
import os

# Set up logging
logging.basicConfig(filename='fetch_us_marinas.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Ensure the output directory exists
output_dir = 'us_marinas_data'
os.makedirs(output_dir, exist_ok=True)

# Define tags for marinas
tags = {'leisure': 'marina'}

# Define coastal states with bounding boxes
coastal_states_regions = {
    "East_Coast": {"north": 47.459686, "south": 24.396308, "east": -66.93457, "west": -81.0},
    "Gulf_Coast": {"north": 31.000968, "south": 24.396308, "east": -81.0, "west": -97.0},
    "West_Coast": {"north": 49.002494, "south": 32.534156, "east": -114.131211, "west": -124.848974},
    "Alaska": {"north": 71.538800, "south": 51.209316, "east": -129.9795, "west": -179.1489},
    "Hawaii": {"north": 28.402123, "south": 18.910361, "east": -154.806773, "west": -178.334698}
}

# Function to fetch and save marina data for a region
def fetch_and_save_marinas(region, tags, index):
    try:
        gdf = ox.features_from_bbox(bbox=(region['north'], region['south'], region['east'], region['west']), tags=tags)
        if not gdf.empty:
            # Save the GeoDataFrame to a file
            filename = f"{output_dir}/marinas_region_{index}.geojson"
            gdf.to_file(filename, driver='GeoJSON')
            logging.info(f"Saved data for region {index} to {filename}")
        else:
            logging.info(f"No data found for region {index}")
    except Exception as e:
        logging.error(f"Error fetching data for region {index}: {e}")

# Fetch and save marina data for each defined region
region_index = 0
for region_name, region in coastal_states_regions.items():
    fetch_and_save_marinas(region, tags, region_index)
    region_index += 1

logging.info("Finished fetching all marina data.")
print("Finished fetching all marina data.")

