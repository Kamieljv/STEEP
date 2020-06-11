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
from shapely.geometry import Point, LineString

class Routing:
    """ Calculates a route between two points at a given time/date, based on the TomTom Route API. """

    def __init__(self):
        # Tomtom url and key
        self.apiURL = "https://api.tomtom.com/routing/1/calculateRoute/"
        self.apiKEY = os.environ.get("TOMTOM_API_KEY")

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

    # Routing function
    def tomtomAPI(self, startLat, startLon, destLat, destLon):
        """ Returns a Geodataframe containing segments and speed """

        tomtomURL = "%s/%s,%s:%s,%s/json?key=%s" % (self.apiURL, startLat, startLon, destLat, destLon, self.apiKEY)
        headers = {
            'accept': '*/*',
        }

        params = dict(
            instructionsType='text',
            language='en-GB',
            # maxAlternatives='3',
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
        # Request and response
        resp = requests.get(tomtomURL, params=params, headers=headers)
        data = resp.json()

        # Transform data object to string
        string = str(data)
        routing = literal_eval(string)

        # Extract points stored in legs (long route, instructions, distance and time) using find function
        lr_points = list(self.find('points', routing))
        long_route = lr_points[0]
        seg_points = list(self.find('point', routing))
        distance = list(self.find('routeOffsetInMeters', routing))
        all_time = list(self.find('travelTimeInSeconds', routing))
        time = all_time[2:]

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

        # Segments
        idlist = []
        for i in range(df_seg.shape[0]):
            searcher = df_seg.iloc[i]
            id = df_long[(df_long['latitude'] == searcher['latitude']) & (
                        df_long['longitude'] == searcher['longitude'])].index.values[0]
            idlist.append(id)

        # Match with speed
        init = 0
        df_long["speed_km/h"] = ''
        for t, i in enumerate(idlist):
            for j in range(init, i):
                df_long.loc[j] = df_speed.iloc[t - 1].values[0]
            init = i
        df_long.loc[i] = df_speed.iloc[t - 1].values[0]

        # Create ID column
        df_long['ID'] = (df_long['speed_km/h']).astype('category').cat.codes

        # Zip the coordinates into a point object and convert to a GeoDataFrame
        geom = [Point(xy) for xy in zip(df_long.longitude, df_long.latitude)]
        long_routeGDF = gpd.GeoDataFrame(df_long, geometry=geom)

        # Matching points
        gpd_line = long_routeGDF.groupby(['speed_km/h', 'ID'])['geometry'].apply(
            lambda x: LineString(x.tolist()) if x.size > 1 else x.tolist())

        # Geodataframe
        gpd_line = gpd.GeoDataFrame(gpd_line)

        return gpd_line

