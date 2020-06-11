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

distance = list(find('routeOffsetInMeters', routing))
all_time = list(find('travelTimeInSeconds', routing))
time = all_time[2:] #can be improverd later

# Calculate distance and time
def calculate(data):
    data_list = []
    for i in range(len(data)):
        if i < len(data) - 1:
            data_sub = abs(data[i] - data[i+1])
            data_list.append(data_sub)
    return data_list

dis_list = calculate(distance)
time_list = calculate(time)

# Calculate speed
import pandas as pd

df_dis = pd.DataFrame(dis_list)
df_time = pd.DataFrame(time_list)
df_speed = (df_dis / df_time) * 3.6

# Long route and segment points as dataframe
seg_points = list(find('point', routing))
long_points = list(find('points', routing))
long_points = long_points[0]
df_seg = pd.DataFrame(seg_points)
df_long = pd.DataFrame(long_points)

# Split
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

# Create ID column
df_long['ID'] = (df_long['speed_km/h']).astype('category').cat.codes

