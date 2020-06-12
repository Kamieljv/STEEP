""" routing.py

    Calculates a route between two points at a given time/date, based on the TomTom Route API.

    Required packages:
    - requests
    - pandas
    - geopandas
    - shapely

"""

import os
import requests
from ast import literal_eval
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, MultiPoint
from shapely.ops import split, snap

class Routing:
    """ Calculates a route between two points at a given time/date, based on the TomTom Route API. """

    def __init__(self):
        # Tomtom url and key
        self.apiURL = "https://api.tomtom.com/routing/1/calculateRoute/"
        self.apiKEY = "x7b42zLGbh4VoCVGHgrDNjC2FKo2hZDo" #os.environ.get("TOMTOM_API_KEY")
        if not self.apiKEY:
            raise Exception("'TOMTOM_API_KEY' not found in environment.")

    def find(self, key, dictionary):
        """ Function to extract data from JSON API response """
        for k, v in dictionary.items():
            if k == key:
                yield v
            elif isinstance(v, dict):
                for result in self.find(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    if isinstance(d, dict):
                        for result in self.find(key, d):
                            yield result

    def decumulate(self, data):
        """ Separates accumulated distance or time values into separate, per-segment values """
        data_list = []
        for i in range(len(data)):
            if i < len(data) - 1:
                data_sub = abs(data[i] - data[i+1])
                data_list.append(data_sub)
        return data_list

    def api_call(self):
        """ Makes the TomTom API call """

        tomtomURL = "%s/%f,%f:%f,%f/json?key=%s" % (self.apiURL, self.startLat, self.startLon, self.destLat, self.destLon, self.apiKEY)
        headers = {
            'accept': '*/*',
        }

        params = dict(
            departAt=self.departure,
            instructionsType='text',
            language='en-GB',
            sectionType='traffic',
            routeRepresentation='polyline',
            report='effectiveSettings',
            routeType='eco',
            traffic='true',
            avoid='unpavedRoads',
            travelMode='car',
            vehicleCommercial='false',
            vehicleEngineType='combustion',
        )
        # Make request
        return requests.get(tomtomURL, params=params, headers=headers).json()

    def get_route(self, startLat, startLon, destLat, destLon, departure):
        """ Returns a Geodataframe containing segments and speed """

        self.startLat = startLat
        self.startLon = startLon
        self.destLat = destLat
        self.destLon = destLon
        self.departure = departure

        response = self.api_call()
        if 'error' in response:
            raise Exception(response['error']['description'])

        # Extract points stored in legs (long route, instructions, distance and time) using find function
        long_route = list(self.find('points', response))[0]
        seg_points = list(self.find('point', response))
        distance = list(self.find('routeOffsetInMeters', response))
        time = list(self.find('travelTimeInSeconds', response))[2:]

        # Dataframe for the long route and the segment points
        df_long = pd.DataFrame(long_route)
        df_seg = pd.DataFrame(seg_points)

        # Calculate distance and time
        dis_list = self.decumulate(distance)
        time_list = self.decumulate(time)

        # Calculate speed
        df_dis = pd.DataFrame(dis_list)
        df_time = pd.DataFrame(time_list)
        df_speed = (df_dis / df_time) * 3.6

        # Zip the route coordinates into a point list and convert to LineString
        routePoints = [Point(x, y) for x, y in zip(df_long.longitude, df_long.latitude)]
        routeLine = LineString(routePoints)

        # Convert segment coordinates to MultiPoint object
        segmentPoints = MultiPoint([Point(x, y) for x, y in zip(df_seg.longitude, df_seg.latitude)])

        # Define a tolerance of roughly 1m
        tolerance = 0.000005

        # snap and split segment points on route line
        split_line = split(routeLine, snap(segmentPoints, routeLine, tolerance))

        # transform resulting Geometry Collection to GeoDataFrame
        segments = [feature for feature in split_line]
        gdf_segments = gpd.GeoDataFrame(list(range(len(segments))), geometry=segments)
        gdf_segments.columns = ['index', 'geometry']

        # Add speed (km/h) and distance (m) column
        gdf_segments = gdf_segments.assign(speed=df_speed, distance=df_dis)

        return gdf_segments