# Map matching test
# Map matching Mapbox

from mapbox import Geocoder
from mapbox import MapMatcher

geocoder = Geocoder(access_token="pk.eyJ1IjoiYm93dHJ1Y2tsZSIsImEiOiJja2IxNXJ1MGcwZXI0MzBxamR0YnYwZ2xmIn0.8vfAlwVcrPvp4J9-W8nIkA")
service = MapMatcher()

#
line = {
    "type": "Feature",
    "geometry": {
        "type": "LineString",
        "coordinates": [
            [13.418946862220764, 52.50055852688439],
            [13.419011235237122, 52.50113000479732],
            [13.419756889343262, 52.50171780290061],
            [13.419885635375975, 52.50237416816131],
            [13.420631289482117, 52.50294888790448]
        ]
    }
}

# Match the LineString to a profile
response = service.match(line, profile='mapbox.driving')
# response.status_code
# response.headers['Content-Type']

# Geojson
corrected = response.geojson()['features'][0]
# corrected['geometry']['type']
# corrected['geometry'] == line['geometry']
# len(corrected['geometry']) == len(line['geometry'])