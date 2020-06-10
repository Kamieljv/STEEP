""" routing.py

    Required packages:
    - requests
    - pandas
    - geopandas

    Usage:
    Start Tomtom API by running:
        $ python routing.py

"""

import requests
from ast import literal_eval
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString

# Tomtom url and key
apiURL = "https://api.tomtom.com/routing/1/calculateRoute/"
apiKEY = "x7b42zLGbh4VoCVGHgrDNjC2FKo2hZDo"

# Coordinates
startLat = 52.533558
startLon = 13.384116
destLat = 52.498929
destLon = 13.41774

def tomtomAPI(apiURL, startLat, startLon, destLat, destLon, apiKEY):
    """
    Returns Tomtom API response
    """
    tomtomURL = "%s/%s,%s:%s,%s/json?key=%s" % (apiURL, startLat, startLon, destLat, destLon, apiKEY)
    headers = {
        'accept': '*/*',
    }
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
    return data

data = tomtomAPI(apiURL, startLat, startLon, destLat, destLon, apiKEY)

## Extract data from API response
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

# Transform data object to string
string = str(data)
routing = literal_eval(string)

# Extract points stored in legs (long route, instructions, distance and time)
lr_points = list(find('points', routing))
long_route = lr_points[0]
seg_points = list(find('point', routing))
distance = list(find('routeOffsetInMeters', routing))
all_time = list(find('travelTimeInSeconds', routing))
time = all_time[2:] #can be improverd later

# Make Geodataframe function
def geodataframe(points_list):
    """
    It makes a geodataframe using the data extracted from the API response
    """
    # Make dataframe
    df = pd.DataFrame(points_list)
    # Make geometry
    geom = [Point(xy) for xy in zip(df['latitude'], df['longitude'])]
    # Creates geodataframe
    df_gd = gpd.GeoDataFrame(df, geometry=geom)
    return df_gd


# Geodataframe for the long route and the segments
lr_gpd = geodataframe(long_route)
seg_gpd = geodataframe(seg_points)

## Segments


## Matching points
def matchingPoints(points_seg):
    line = points_seg.groupby(['ID', 'speed'])['geometry'].apply(lambda x: LineString(x.tolist()))
    gpd_line = gpd.GeoDataFrame(line, geometry=geometry)
    return gpd_line


## Calculations (distance, time, speed)
def calculate(data):
    data_list = []
    for i in range(len(data)):
        if i < len(data) - 1:
            data_sub = abs(data[i] - data[i+1])
            data_list.append(data_sub)
    return data_list

# Calculate distance and time
dis_list = calculate(distance)
time_list = calculate(time)

# Speed function
def speed(dis_list, time_list, geo_dataframe):
    df_dis = pd.DataFrame(dis_list)
    df_time = pd.DataFrame(time_list)
    speed_calc = (df_dis /df_time) * 3.6
    df_speed = speed_calc.fillna(0)
    geo_dataframe['speed_km/h'] = df_speed
    return df_speed


# Geodataframe with speed
geometry = [Point(xy) for xy in zip(df_point['latitude'], df_point['longitude'])]
routingGDF = gpd.GeoDataFrame(df_point, geometry=geometry)

