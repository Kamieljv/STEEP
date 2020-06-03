# Routing
# Map Matching API

## Perform the imports
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['key'] = '3fccaaf9-1e62-4a69-ae2c-7c4ec49ec955'

# Create an instance of the API class
api_instance = swagger_client.MapMatchingApi(swagger_client.ApiClient(configuration))

try:
    # Map-match a GPX file
    api_response = api_instance.post_gpx()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MapMatchingApi->post_gpx: %s\n" % e)