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
    maxAlternatives='3',
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


data = list(find('points', routing))
data = data[0]

# Store as geodataframe
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

df = pd.DataFrame(data)
my_columns = ['lon', 'lat']
df.columns = my_columns
print(df.head)

geometry = [Point(xy) for xy in zip(df['lon'], df['lat'])]
routingGDF = gpd.GeoDataFrame(df, geometry=geometry)
routingGDF.crs = {'init': 'epsg:28992'}
routingGDF.plot(marker='.', color='green', markersize=50)
print(type(routingGDF), len(routingGDF))


