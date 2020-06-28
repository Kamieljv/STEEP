""" api_setup.py

    Usage:
    This script tests the connection to the TomTom API.
    This script is meant to run independently.

"""

from datetime import datetime, timedelta
import pytz
import geopandas as gpd

print("Starting API test...")

# Import the routing library (src/routing.py) where the API is initialized
print("Importing custom routing library from src/routing.py...")
from src.routing import Routing
router = Routing()

print("Checking presence of API key...")
if router.has_key():
    print("API key present")
else:
    raise Exception("No API key configured. Get an API key on https://developer.tomtom.com/ and set it in 'src/routing.py'.")

print("Testing API with sample route...")
# Calculate route
startLat, startLon = 52.3731, 4.8965 # Amsterdam, North Holland, The Netherlands
destLat, destLon = 52.0859, 5.1201 # Utrecht, North Holland, The Netherlands
print("\tStart coordinates: {}, {}".format(startLat, startLon))
print("\tDestination coordinates: {}, {}".format(destLat, destLat))

# Define and format the departure time variable
tz = pytz.timezone('Europe/Amsterdam') # set time zone
fmt = '%Y-%m-%dT%H:%M:%S%z' # set date format
dep_string = tz.localize(datetime.now() + timedelta(minutes=1)).strftime(fmt) # set departure 1 minute from now and convert to string format
dep_string = dep_string[:-2] + ':' + dep_string[-2:] # extra formatting to comply to TomTom API requirements
print("\tDeparture: " + dep_string)
routetype = "fastest"
print("\tRoutetype: " + routetype)
traffic = True
print("\tTraffic: " + ("enabled" if traffic else "disabled"))
route = router.get_route(startLat, startLon, destLat, destLon, dep_string, routetype, traffic)

print("\nRoute Calculated!")
print("\tDistance: " + str(round(route['distance'].sum() / 1000, 2)) + " km")
print("\tTime: " + str(round(route['time'].sum() / 60, 2)) + " min")

if isinstance(route, gpd.GeoDataFrame) and route.length is not 0:
    print("\nTest Successful")





