""" scenario_builder.py

    Required packages:
    - pandas
    - pytz
    - numpy


    The class(es) in this document are loaded by 'app.py'.
    This class performs the necessary operations to build and run a scenario and report the statistics to the user.
"""
from src.emission_calculator import EmissionCalculator
from src.routing import Routing
import pandas as pd
import pytz, random
import numpy as np
from datetime import datetime, timedelta

class Scenario:
    """Used for building, running and reporting on scenarios."""

    def __init__(self, callLimit=20, **kwargs):
        """ Initializes the class"""
        self.callLimit = callLimit
        self.expected = ['start', 'start-coords', 'dest', 'dest-coords', 'route-type', 'fuel', 'segment', 'standard', \
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
        self.traffic = 'traffic' in kwargs
        self.commuters = int(self.commuters)
        self.fmt = '%Y-%m-%dT%H:%M:%S%z'  # set date format
        self.tz = pytz.timezone('Europe/Amsterdam')  # set time zone

    def listDepartures(self):
        # Define a dictionary to convert weekday numbers to pandas weekday codes
        self.day_conv = {0: 'W-MON', 1: 'W-TUE', 2: 'W-WED', 3: 'W-THU', 4: 'W-FRI', 5: 'W-SAT', 6: 'W-SUN'}
        start, end = self.daterange.split(" to ")
        departures = []

        for i in self.weekdays.split(","):
            dates = pd.date_range(start=start, end=end, freq=self.day_conv[int(i)]).tolist()
            departures += [self.tz.localize(date).strftime(self.fmt) for date in dates]

        self.departures = [d[:11] + self.departuretime + d[16:22] + ":" + d[22:] for d in departures]
        self.departures += [d[:11] + self.returntime + d[16:] for d in self.departures]

        self.departures.sort()

    def run(self, write=False):
        """ Run the scenario from the list of departures.
            - Returns:
                * padndas dataframe with scenario results;
                * path string to point to a csv save of that dataframe
        """
        # Check if we are not making too many API calls
        self.listDepartures()
        if len(self.departures) > self.callLimit:
            return {'error': 'Number of API calls ('+ str(len(self.departures)) +') exceeds limit (' + str(self.callLimit) + '). Please reduce the length of the Date range or number of Commute days.'}

        # Define dataframe to store results
        cols = ['departure', 'emissions', 'distance', 'time', 'routetype', 'fuel', 'segment', 'standard',
                'start', 'startLat', 'startLon', 'dest', 'destLat', 'destLon']
        self.df_results = pd.DataFrame(columns=cols)

        # Run the routing algorithm
        router = Routing() # Initialize router class
        for departure in self.departures:
            route = router.get_route(self.startLat, self.startLon, self.destLat, self.destLon, departure,
                                 self.routetype, self.traffic)

            # Calculate emissions
            calculator = EmissionCalculator(fuel=self.fuel, segment=self.segment, standard=self.standard)
            calculator.calculate_ec_factor(route)
            stats = np.array(calculator.calculate_stats())
            df_row = pd.DataFrame([[departure] + list(stats) + \
                                   [self.routetype, self.fuel, self.segment, self.standard, \
                                    self.start, self.startLat, self.startLon, \
                                    self.dest, self.destLat, self.destLon]], columns=cols)
            self.df_results = self.df_results.append(df_row)

        # Create and write to file, with datestamp and hash in name, for security
        if write:
            self.fpath = 'output/scenario-results_' + datetime.strftime(datetime.now(), '%Y%m%dT%H%M') + '_%016x.csv' % random.getrandbits(64)
            self.df_results.to_csv(self.fpath, index=False)

    def read(self, path):
        """ Read scenario from a logged file. """

        self.listDepartures()
        self.df_results = pd.read_csv(path)

    def durationOverSlots(self, df_row):
        """ Takes trip departure time and duration and spreads it out over multiple one-hour timeslots, with homogeneous emissions.
            - df_row [pandas dataframe]: single dataframe row with timestamp index and time and emission value.
        """
        start = df_row.index[0]
        min = start.replace(minute=0) # round minimum time down to hour
        end = start + timedelta(seconds=int(df_row.time.values[0])) # define the end of the trip
        max = end.replace(minute=0, second=0) # round maximum time down to hour
        slot_index = pd.date_range(min, max, freq='H')
        slots = pd.Series(index=slot_index, dtype=float)

        # define checkpoint to be either the end time (if that falls in the same hour as start) or the first hour-mark
        check = end if len(slots) <= 1 else slots.index[1]

        # assign emissions to the first slot (formula: time in slot / trip time * emissions)
        slots.iloc[[0]] = (check - start).seconds / df_row.time.values[0] * df_row.emissions.values[0]

        # loop over times in index that divide the trip emissions
        if len(slots) > 1:
            for i, divider in enumerate(slots[1:]):
                if i == len(slots[1:]) - 1:
                    slots.iloc[[-1]] = (end - max).seconds / df_row.time.values[0] * df_row.emissions.values[0]
                else:
                    slots.iloc[[i+1]] = (slot_index[i+1] - slot_index[i]).seconds / df_row.time.values[0] * df_row.emissions.values[0]

        return slots

    def timeseries(self):
        """ Calculates an accumulated emissions time-series. """
        # Convert results dataframe to time-series
        df_res = self.df_results  # copy results dataframe
        df_res.index = pd.to_datetime(df_res['departure'], format=self.fmt)
        df_res = df_res.drop(columns=['departure'])
        # Convert distance and time columns to numeric
        df_res[['distance', 'time']] = df_res[['distance', 'time']].apply(pd.to_numeric)

        # Create pandas time series object from min and max date
        index = pd.date_range(df_res.index[0].date(), df_res.index[-1].date() + timedelta(days=1), freq='H', tz=self.tz)
        tseries = pd.Series(index=index[:-1], dtype=float)

        for i in range(len(df_res)):
            slots = self.durationOverSlots(df_res.iloc[[i]])
            tseries[slots.index] = slots.values

        # Fill NaN values with zeros
        tseries = tseries.fillna(0.0)

        return tseries
