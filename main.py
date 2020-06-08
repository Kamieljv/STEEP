## Perform the imports
from __future__ import print_function
import swagger_client
import swagger_client.configuration as config
from swagger_client.rest import ApiException
from pprint import pprint

## Configure API key authorization: api_key
configuration = config.Configuration()
configuration.api_key['key'] = '300e1077-dc69-4d98-ba69-dc947e1f9228' # we are using another key for this branch

## create an instance of the API class
api_instance = swagger_client.RouteOptimizationApi(swagger_client.ApiClient(configuration))
body = swagger_client.Request(
    vehicles=[swagger_client.Vehicle(
        vehicle_id='my_vehicle',
        type_id='car_type',
        start_address=swagger_client.Address(
            location_id='Berlin',
            lon=13.406,
            lat=52.537
        ),
        return_to_depot=False
    )],
    vehicle_types=[swagger_client.VehicleType(
        type_id='car_type',
        profile='car'
    )],
    services=[swagger_client.Service(
        id='hamburg',
        name='visit_hamburg',
        address=swagger_client.Address(
            location_id='Hamburg',
            lon=9.999,
            lat=53.552
        )
    )],
    configuration=swagger_client.models.configuration.Configuration(
        routing=swagger_client.Routing(
            calc_points=True,
            consider_traffic=True,
        )
    )
)

## Set parameters for request

## Make API call for solver
try:
    # Execute a routing request
    api_response = api_instance.solve_vrp(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RouteOptimizationAPI->solve_vrp: %s\n" % e)

## Fetch result
api_instance = swagger_client.RouteOptimizationApi(swagger_client.ApiClient(configuration))
job_id = api_response.job_id

try:
    # Retrieve solution
    api_response = api_instance.get_solution(job_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RouteOptimizationApi->get_solution: %s\n" % e)
##

# Extract data
from ast import literal_eval

string = str(api_response)
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


data = list(find('coordinates', routing))
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




