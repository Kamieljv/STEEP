## Perform the imports
from __future__ import print_function
import swagger_client
import swagger_client.configuration as config
from swagger_client.rest import ApiException
from pprint import pprint

## Configure API key authorization: api_key
configuration = config.Configuration()
configuration.api_key['key'] = '3fccaaf9-1e62-4a69-ae2c-7c4ec49ec955'


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
    )]
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

