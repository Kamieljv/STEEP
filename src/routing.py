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
startLat = 52.514426
startLon = 13.315560
destLat = 52.510458
destLon = 13.286269

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

# Extract data from API response
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

# Extract points stored in legs (long route, instructions, distance and time) using find function
lr_points = list(find('points', routing))
long_route = lr_points[0]
seg_points = list(find('point', routing))
distance = list(find('routeOffsetInMeters', routing))
all_time = list(find('travelTimeInSeconds', routing))
time = all_time[2:]

# Dataframe for the long route and the segment points
df_long = pd.DataFrame(long_route)
df_seg = pd.DataFrame(seg_points)

# Calculations (distance, time, speed)
def calculate(data):
    """
    Returns a list of the object to calculate
    """
    data_list = []
    for i in range(len(data)):
        if i < len(data) - 1:
            data_sub = abs(data[i] - data[i+1])
            data_list.append(data_sub)
    return data_list

# Calculate distance and time
dis_list = calculate(distance)
time_list = calculate(time)

# Calculate speed
df_dis = pd.DataFrame(dis_list)
df_time = pd.DataFrame(time_list)
df_speed = (df_dis / df_time) * 3.6

# Segments
idlist=[]
for i in range(df_seg.shape[0]) :
    searcher=df_seg.iloc[i]
    id =df_long[(df_long['latitude'] == searcher['latitude']) & (df_long['longitude'] == searcher['longitude'])].index.values[0]
    idlist.append(id)

# Match with speed
init=0
df_long["speed_km/h"]=''
for t,i in enumerate(idlist):
    for j in range(init,i):
        df_long.loc[j]=df_speed.iloc[t-1].values[0]
    init=i
df_long.loc[i] = df_speed.iloc[t-1].values[0]

# Zip the coordinates into a point object and convert to a GeoDataFrame
geom = [Point(xy) for xy in zip(df_long.longitude, df_long.latitude)]
long_routeGDF = gpd.GeoDataFrame(df_long, geometry=geom)

# Matching points
gpd_line = long_routeGDF.groupby(['speed_km/h'])['geometry'].apply(lambda x: LineString(x.tolist())if x.size > 1 else x.tolist())
gpd_line = gpd.GeoDataFrame(gpd_line)





