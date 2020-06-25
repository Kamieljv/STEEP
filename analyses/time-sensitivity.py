""" time-sensitivity.py

    Required packages:
    - pytz
    - csv
    - datetime
    - matplotlib

    Usage:

    This script is meant to run independently.

"""

import pandas as pd
import matplotlib.pyplot as plt
import pytz, csv
from datetime import datetime, timedelta
from src.routing import Routing
from src.emission_calculator import EmissionCalculator

def timeProfileLoop(date, timestep=10, days=1):
    """ Function to loop through a 24 hour day with a given time step and calculate the route and stats between two points.
        - date [string as '%Y-%m-%d %H:%M']: date on which to carry out the analysis (has to be future date!)
        - timestep [int]: time in minutes between each departure
        - days [int]: number of days for which the
    """
    # Convert date input to datetime object
    departure = datetime.strptime(date, '%Y-%m-%d %H:%M')
    maxdate = departure + timedelta(days=days)
    # Calculate route
    startLat, startLon = 52.3731, 4.8965
    destLat, destLon = 52.0859, 5.1201

    # Define and format the departure time variable
    tz = pytz.timezone('Europe/Amsterdam') # set time zone
    fmt = '%Y-%m-%dT%H:%M:%S%z' # set date format

    # Define dataframe for time profile
    cols = ['departure', 'emissions', 'distance', 'time', 'routetype', 'fuel', 'segment', 'standard', 'startLat', 'startLon', 'destLat', 'destLon']
    df_timeprofile = pd.DataFrame(columns=cols)

    routetype = 'fastest'

    # Start time loop
    while departure <= maxdate:
        departure += timedelta(minutes=timestep)

        dep_string = tz.localize(departure).strftime(fmt)
        dep_string = dep_string[:-2] + ':' + dep_string[-2:]

        router = Routing()
        route = router.get_route(startLat, startLon, destLat, float(destLon), dep_string, routetype=routetype, traffic=True)

        # Initialize calculator with COPERT model file
        fuel, segment, standard = ("Petrol", "Small", "Euro 5")
        calculator = EmissionCalculator(fuel=fuel,
                                        segment=segment,
                                        standard=standard, root="../")

        calculator.calculate_ec_factor(route)
        stats = calculator.calculate_stats()
        df_row = pd.DataFrame([[dep_string] + list(stats) + [routetype, fuel, segment, standard, startLat, startLon, destLat, destLon]], columns=cols)
        df_timeprofile = df_timeprofile.append(df_row)

        df_timeprofile.to_csv('output/timeprofile_'+ datetime.strftime(datetime.now(), '%Y%m%dT%H%M') +'.csv', index=False)

def plotTimeProfile(file):

    # Read from csv file into pandas dataframe
    df_timeprofile = pd.read_csv(file, index_col=0, parse_dates=True)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)

    df_timeprofile['time'].plot(ax=ax1)
    ax1.set_title('Time')
    df_timeprofile['emissions'].plot(ax=ax2)
    ax2.set_title('Emissions')
    df_timeprofile['distance'].plot(ax=ax3)
    ax3.set_title('Distance')

    plt.show()


if __name__ == '__main__':
   # timeProfileLoop("2020-07-01 00:00", timestep=60, days=1)
    plotTimeProfile('output/timeprofile_20200625T1524.csv')