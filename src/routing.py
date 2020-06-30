""" routing.py

    Calculates a route between two points at a given time/date, based on the TomTom Route API.

    Required packages:
    - requests
    - pandas
    - geopandas
    - shapely

"""

import requests
import pandas as pd
import geopandas as gpd
from geopandas import GeoSeries
from shapely.geometry import Point, LineString, MultiPoint
from shapely.ops import nearest_points
import pytz, re
from datetime import datetime, timedelta

class Routing:
    """ Calculates a route between two points at a given time/date, based on the TomTom Route API. """

    def __init__(self):
        # Tomtom url and key
        self.apiURL = "https://api.tomtom.com/routing/1/calculateRoute/"
        self.apiKEY = ""
        if not self.apiKEY or self.apiKEY == "":
            raise Exception("'TOMTOM_API_KEY' not specified.")
        self.tz = pytz.timezone('Europe/Amsterdam')

    def has_key(self):
        if not self.apiKEY or self.apiKEY == "":
            raise Exception("'TOMTOM_API_KEY' not specified.")
        else:
            return True

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
            routeType=self.routetype,
            traffic=str(self.traffic).lower(),
            avoid='unpavedRoads',
            travelMode='car',
            vehicleCommercial='false',
            vehicleEngineType='combustion',
        )
        # Make request
        return requests.get(tomtomURL, params=params, headers=headers).json()

    def get_route(self, startLat, startLon, destLat, destLon, departure, routetype, traffic):
        """ Returns a Geodataframe containing segments and speed """

        self.startLat = startLat
        self.startLon = startLon
        self.destLat = destLat
        self.destLon = destLon
        self.departure = departure
        self.routetype = routetype
        self.traffic = traffic

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
        segmentPoints_geoseries = GeoSeries(segmentPoints)

        # snap and split segment points on route line
        split_line = self.cut_line_at_points(routeLine, segmentPoints)

        # transform resulting Geometry Collection to GeoDataFrame
        segments = [feature for feature in split_line]
        gdf_segments = gpd.GeoDataFrame(list(range(len(segments))), geometry=segments)
        gdf_segments.columns = ['index', 'geometry']

        # Add speed (km/h) and distance (m) column
        gdf_segments = gdf_segments.assign(speed=df_speed, distance=df_dis, time=df_time)

        return gdf_segments

    def cut_line_at_points(self, line, points):
        # First coords of line
        coords = list(line.coords)

        # Keep list coords where to cut (cuts = 1)
        cuts = [0] * len(coords)
        cuts[0] = 1
        cuts[-1] = 1

        # Add the coords from the points
        points_proj = [nearest_points(line, p)[0] for p in points]
        coords += [list(p.coords)[0] for p in points_proj]
        cuts += [1] * len(points)

        # Calculate the distance along the line for each point
        dists = [line.project(Point(p)) for p in coords]

        # sort the coords/cuts based on the distances
        # see http://stackoverflow.com/questions/6618515/sorting-list-based-on-values-from-another-list
        coords = [p for (d, p) in sorted(zip(dists, coords))]
        cuts = [p for (d, p) in sorted(zip(dists, cuts))]

        # generate the Lines
        # lines = [LineString([coords[i], coords[i+1]]) for i in range(len(coords)-1)]
        lines = []

        for i in range(len(coords) - 1):
            if cuts[i] == 1:
                # find next element in cuts == 1 starting from index i + 1
                j = cuts.index(1, i + 1)
                lines.append(LineString(coords[i:j + 1]))

        return lines[1:-1]

    def timewindow(self, departure, outFormat='%Y-%m-%dT%H:%M:%S%z'):
        """ Gives a time window around the chosen departure time, returning a list of departure times.
            - departure [datetime object]: datetime object of departure
            - outFormat [string]: format of the outgoing departure data
        """
        future_tw = True
        # Check if departure is far enough into the future to make two-sided time-window
        if departure - timedelta(minutes=11) >= datetime.now(self.tz):
            departure -= timedelta(minutes=10)
            future_tw = False

        # Create time window
        departures = []
        departures.append(datetime.strftime(departure, '%Y-%m-%d %H:%M'))
        for i in range(4):
            departure += timedelta(minutes=5)
            departures.append(datetime.strftime(departure, '%Y-%m-%d %H:%M'))

        dep_fmt = []
        for dep in departures:
            # Define and format the departure time variable
            t = [int(x) for x in re.split(' |-|:', dep)]  # convert to integers
            departure = self.tz.localize(datetime(t[0], t[1], t[2], t[3], t[4], 0)).strftime(outFormat)
            departure = departure[:-2] + ':' + departure[-2:]
            dep_fmt.append(departure)

        return dep_fmt, future_tw