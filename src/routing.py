# openrouteservice 2.3.0

# Performing imports
import openrouteservice as ors
import requests

# Making a POST request
r = requests.post('https://api.openrouteservice.org/v2/directions/driving-car/geojson', data ={'key':'value'})

# Some coordinates in Berlin
coordinates = [[13.384116, 52.533558], [13.41774, 52.498929], [13.428726, 52.519355], [13.374825, 52.496369]]
client = ors.Client(key='5b3ce3597851110001cf6248c57990f293fd4de19877a58572bbceeb')

route = client.directions(coordinates=coordinates,
                          profile='driving-car',
                          format='geojson',
                          validate=False,
                          extra_info='AvgSpeed')




