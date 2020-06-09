# STEEP
# Inselberg
# Route

## Tomtom Calculate route API

# Performing imports
import requests
from ast import literal_eval
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Tomtom url and key
apiURL = "https://api.tomtom.com/routing/1/calculateRoute/"
apiKEY = "x7b42zLGbh4VoCVGHgrDNjC2FKo2hZDo"

# Coordinates
sourceLat = 52.533558
sourceLon = 13.384116
destLat = 52.498929
destLon = 13.41774

# Tomtom url
tomtomURL = "%s/%s,%s:%s,%s/json?key=%s" % (apiURL, sourceLat, sourceLon, destLat, destLon, apiKEY)

# Headers
headers = {
    'accept': '*/*',
}

# Parameters
params = dict(
    instructionsType='text',
    language='en-GB',
    # maxAlternatives='3',
    sectionType='traffic',
    routeRepresentation='polyline',
    report='effectiveSettings',
    routeType='eco',
    traffic='true',
    avoid='unpavedRoads',
    travelMode='car',
    vehicleCommercial='false',
    vehicleEngineType='combustion',
)

# Request and response
resp = requests.get(tomtomURL, params=params, headers=headers)
data = resp.json()

## Extract data from API response
# Transform data object to string
string = str(data)
routing = literal_eval(string)


# Function to find key in a dictionary
def find(key, dictionary):
    for k, v in dictionary.items():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                if isinstance(d, dict):
                    for result in find(key, d):
                        yield result


# Extract points stored in legs
lr_points = list(find('points', routing))
long_route = lr_points[0]

# Extract points from the instructions section
seg_points = list(find('point', routing))

# Initialize our 2 arrays that will contain all the points of the long route
lat_lr = []
long_lr = []

# Iterate through all the points and add the lat and long to the correct array (long route)
for point in long_route:
    lat_lr.append(point['latitude'])
    long_lr.append(point['longitude'])

# Initialize our 2 arrays that will contain all the points of the segmented route
lat_seg = []
long_seg = []

# Iterate through all the points and add the lat and long to the correct array (segmented route)
for point in seg_points:
    lat_seg.append(point['latitude'])
    long_seg.append(point['longitude'])


## Make a geodataframe

# Make Geodataframe function
def geodataframe(long, lat, column_long, column_lat):
    # arg: Longitude and latitude points in a list and the name of the columns for each list
    # fun: It makes a geodataframe using the coordinates list

    # Make dataframe
    df = pd.DataFrame([long, lat])
    df = pd.DataFrame.transpose(df)
    df.columns = [column_long, column_lat]

    # Make geometry
    geometry = [Point(xy) for xy in zip(df[column_long], df[column_lat])]

    # Creates geodataframe
    df_gd = gpd.GeoDataFrame(df, geometry=geometry)

    return df_gd


# Geodataframe for the long route and the segments
lr_gpd = geodataframe(long_lr, lat_lr, 'longitude', 'latitude')
seg_gpd = geodataframe(long_seg, lat_seg, 'longitude', 'latitude')

# Geodataframe visualization
lr_gpd.crs = {'init': 'epsg:28992'}
lr_gpd.plot(marker='*', color='green', markersize=50)
print(type(lr_gpd), len(lr_gpd))

seg_gpd.crs = {'init': 'epsg:28992'}
seg_gpd.plot(marker='*', color='green', markersize=50)
print(type(seg_gpd), len(seg_gpd))

## Segments
