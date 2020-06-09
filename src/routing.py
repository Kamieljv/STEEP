## STEEP
## Inselberg
## Route

## Tomtom Calculate route API

# Performing imports
import requests

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

# Request and response
resp = requests.get(tomtomURL, params=params, headers=headers)
data = resp.json()

## Extract data from API response
# Performing imports
from ast import literal_eval

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
points_lr = list(find('points', routing))
long_route = points_lr[0]

# Extract points in instructions
points_edg = list(find('point', routing))

#



