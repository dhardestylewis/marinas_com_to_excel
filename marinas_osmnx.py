import osmnx as ox
import json

# Specify the location or bounding box for the query
# For example, let's use a bounding box for New York City
north, south, east, west = 40.917577, 40.477399, -73.700272, -74.259090

# Fetch marina data with the leisure=marina tag
tags = {'leisure': 'marina'}
gdf = ox.geometries_from_bbox(north, south, east, west, tags)

# Convert the GeoDataFrame to JSON
data = gdf.to_json()

# Pretty-print the JSON data
pretty_json = json.dumps(json.loads(data), indent=4)

# Save the pretty-printed JSON to a file
with open('marinas.json', 'w') as file:
    file.write(pretty_json)

# Print the pretty-printed JSON
print(pretty_json)

