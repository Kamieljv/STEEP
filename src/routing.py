### test
import requests

apiURL = 'http://maps.googleapis.com/maps/api/directions/json'
apiKEY = "x7b42zLGbh4VoCVGHgrDNjC2FKo2hZDo"

# Coordinates
sourceLat = 52.533558
sourceLon = 13.384116
destLat = 52.498929
destLon = 13.41774

# Tomtom url
tomtomURL = "%s/%s,%s:%s,%s/json?key=%s" % (apiURL, sourceLat, sourceLon, destLat, destLon, apiKEY)

# Parameters
params = dict(
    versionNumber=1,
    location='Berlin:Hamburg',
    maxAlternatives=3,
    alternativeType='betterRoute',
    instructionsType='text',
    language='en-GB',
    routeRepresentation='polyline',
    computeTravelTimeFor='all',
    sectionType='traffic'
)

resp = requests.get(tomtomURL, params=params)
data = resp.json()







