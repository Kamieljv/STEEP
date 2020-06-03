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

import requests
import geopandas as gpd
import osmnx as ox
import matplotlib.pyplot as plt
#place_name = "Berlin"
#graph = ox.graph_from_place(place_name)
#type(graph)
import pandas as pd
from pandas.io.json import json_normalize
import json
import csv
url = 'https://graphhopper.com/api/1/match?vehicle=car&key=3fccaaf9-1e62-4a69-ae2c-7c4ec49ec955\" --data @/path/to/some.gpx' #osm direction api
response = requests.get(url)
data = response.json()
print(data)
df = pd.io.json.json_normalize(data)
def flatten_json(y):
    out = {}

    def flatten(x, name=""):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + "_")
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + "_")
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

flat = flatten_json(data)
dfObj = pd.DataFrame(flat, index=['a'])
dfObj.to_csv(r'D:\Git\github\\test.csv')