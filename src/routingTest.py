# Huanhuan file
# Tomtom Calculate route API
import requests

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
    #maxAlternatives='3',
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

resp = requests.get(tomtomURL, params=params, headers=headers)
data = resp.json()

# Extract data
from ast import literal_eval

string = str(data)
routing = literal_eval(string)


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

seg_points = list(find('point', routing))
distance = list(find('routeOffsetInMeters', routing))
all_time = list(find('travelTimeInSeconds', routing))
time = all_time[2:] #can be improverd later

#calculate distance
dis_list = []
for i in range(len(distance)):
    if i < len(distance) - 1:
        dis = abs(distance[i]-distance[i+1])
        dis_list.append(dis)
#print(dis_list)

#calculate time
time_list = []
for i in range(len(time)):
    if i < len(time) - 1:
        tim = abs(time[i]-time[i+1])
        time_list.append(tim)
#print(time_list)

#calculate speed
#import numpy as np
#dis_ar = np.array(dis_list)
#time_ar = np.array(time_list)
#speed_ar = dis_ar/time_ar
import pandas as pd
df_dis = pd.DataFrame(dis_list)
df_time = pd.DataFrame(time_list)
df_speed = (df_dis /df_time) * 3.6

# Store as geodataframe
import geopandas as gpd
from shapely.geometry import Point
df_point = pd.DataFrame(seg_points)
#my_columns = ['lon', 'lat']
#df.columns = my_columns
print(df_point.head)

# didnt finish
geometry = [Point(xy) for xy in zip(df['lon'], df['lat'])]
routingGDF = gpd.GeoDataFrame(df, geometry=geometry)
routingGDF.crs = {'init': 'epsg:28992'}
routingGDF.plot(marker='.', color='green', markersize=50)
print(type(routingGDF), len(routingGDF))
