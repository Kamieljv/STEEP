# Tomtom API

## Performing imports
import requests
import json
import urllib.request

# URL to the Tomtom API
apiURL = "https://api.tomtom.com/routing/1/calculateRoute/"

# APIkey
apiKEY = "x7b42zLGbh4VoCVGHgrDNjC2FKo2hZDo"

# Coordinates
sourceLat = 52.533558
sourceLon = 13.384116
destLat = 52.498929
destLon = 13.41774

# Adding coordinates to the url
tomtomURL = "%s/%s,%s:%s,%s/json?key=%s" % (apiURL, sourceLat, sourceLon, destLat, destLon, apiKEY)

# Getting data
getData = urllib.request.urlopen(tomtomURL).read()
jsonTomTomString = json.loads(getData)








