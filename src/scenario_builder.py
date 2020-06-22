""" scenario_builder.py

    Required packages:
    - pandas

    The class(es) in this document are loaded by 'app.py'.
    This class performs the necessary operations to build and run a scenario and report the statistics to the user.
"""
from src.emission_calculator import EmissionCalculator
from src.routing import Routing
import pandas as pd
import pytz
from datetime import datetime

class Scenario:
    """Used for building, running and reporting on scenarios."""

    def __init__(self, callLimit=20, **kwargs):
        """ Initializes the class"""
        self.callLimit = callLimit
        self.expected = ['start-coords', 'dest-coords', 'route-type', 'fuel', 'segment', 'standard', \
                         'date-range', 'weekdays', 'departure-time', 'return-time', 'commuters']

        for key, value in kwargs.items():
            if key in self.expected:
                setattr(self, key.replace("-",""), value)

        for key in self.expected:
            try:
                getattr(self, key.replace("-",""))
            except:
                raise Exception("Missing required argument '" + key + "' for scenario. All of the following arguments should be given: "+str(self.expected))

        self.startLat, self.startLon = [float(c) for c in self.startcoords.split(", ")]
        self.destLat, self.destLon = [float(c) for c in self.destcoords.split(", ")]
        self.traffic = 'traffic' in input

    def listDepartures(self):
        # Define a dictionary to convert weekday numbers to pandas weekday codes
        self.day_conv = {0: 'W-MON', 1: 'W-TUE', 2: 'W-WED', 3: 'W-THU', 4: 'W-FRI', 5: 'W-SAT', 6: 'W-SUN'}
        tz = pytz.timezone('Europe/Amsterdam')  # set time zone
        fmt = '%Y-%m-%dT%H:%M:%S%z' # set date format
        start, end = self.daterange.split(" to ")
        departures = []

        for i in self.weekdays.split(","):
            dates = pd.date_range(start=start, end=end, freq=self.day_conv[int(i)]).tolist()
            departures += [tz.localize(date).strftime(fmt) for date in dates]

        self.departures = [d[:11] + self.departuretime + d[16:22] + ":" + d[22:] for d in departures]
        self.departures += [d[:11] + self.returntime + d[16:] for d in self.departures]

        self.departures.sort()
        return self.departures

    def run(self):
        """ Run the scenario from the list of departures. """
        # Check if we are not making too many API calls
        self.listDepartures()
        if len(self.departures) > self.callLimit:
            return {'error': 'Number of API calls exceeds limit (' + str(self.callLimit) + ').'}

        router = Routing() # Initialize router class
        for departure in self.departures:
            route = router.get_route(self.startLat, self.startLon, self.destLat, self.destLon, departure,
                                 self.routetype, self.traffic)

            # Calculate emissions
            calculator = EmissionCalculator(fuel=self.fuel, segment=self.segment, standard=self.standard)
            calculator.calculate_ec_factor(route)
            emissions, distance, time = calculator.calculate_stats()
            print("Route calculated: {} kg CO2, {} km, {} s".format(emissions, distance / 1000, time))

input = {'start': 'Wijchen, Gelderland, Netherlands, The Netherlands', 'start-coords': '51.8099983, 5.7362233',\
         'dest': 'Nijmegen, Gelderland, Netherlands, The Netherlands', 'dest-coords': '51.842574850000005, 5.838960628748229',\
         'route-type': 'eco', 'traffic': 'on', 'fuel': 'Petrol', 'segment': 'Mini', 'standard': 'Euro 4',\
         'date-range':'2020-06-23 to 2020-06-30', 'weekdays': '0,1,2,3,4', 'departure-time': '12:00', 'return-time': '13:00', \
         'commuters': '2'}

scenario = Scenario(**input)
scenario.run()