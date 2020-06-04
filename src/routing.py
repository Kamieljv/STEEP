# openrouteservice 2.3.0

import openrouteservice as ors
import folium
# from openrouteservice.directions import directions

m = folium.Map(location=[52.521861, 13.40744], tiles='cartodbpositron', zoom_start=13)

# Some coordinates in Berlin
coordinates = [[13.384116, 52.533558], [13.41774, 52.498929], [13.428726, 52.519355], [13.374825, 52.496369]]
client = ors.Client(key='5b3ce3597851110001cf6248c57990f293fd4de19877a58572bbceeb')

for idx, coords in enumerate(coordinates):
    folium.Marker(location=list(reversed(coords)),
                 popup=folium.Popup("ID: {}".format(idx))).add_to(m)

route = client.directions(coordinates= coordinates, profile='driving-car',
                           format='geojson', validate=False)

folium.PolyLine(locations=[list(reversed(coord))
                           for coord in
                           route['features'][0]['geometry']['coordinates']]).add_to(m)

m
