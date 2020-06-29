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
        departure += timedelta(minutes=timestep)

    df_timeprofile.to_csv('output/timeprofile_'+ datetime.strftime(datetime.now(), '%Y%m%dT%H%M') +'.csv', index=False)

def plotTimeProfile(file, file2, file3):

    # Read from csv file into pandas dataframe
    df_timeprofile = pd.read_csv(file, index_col=0, parse_dates=True)
    df_timeprofile['time'] = df_timeprofile['time']/60
    df_timeprofile['distance'] = df_timeprofile['distance']/1000
    df_timeprofile2 = pd.read_csv(file2, index_col=0, parse_dates=True)
    df_timeprofile2['time'] = df_timeprofile2['time'] / 60
    df_timeprofile2['distance'] = df_timeprofile2['distance'] / 1000
    df_timeprofile3 = pd.read_csv(file3, index_col=0, parse_dates=True)
    df_timeprofile3['time'] = df_timeprofile3['time'] / 60
    df_timeprofile3['distance'] = df_timeprofile3['distance'] / 1000
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)

    df_timeprofile['time'].plot(ax=ax1, label="10 AM")
    df_timeprofile2['time'].plot(ax=ax1, color='r', label='5 PM')
    df_timeprofile3['time'].plot(ax=ax1, color='g', label='6 PM')
    ax1.set_title('Time')
    ax1.set(xlabel="Date of Departure", ylabel="Travel Time (min)")

    df_timeprofile['emissions'].plot(ax=ax2, label="10 AM")
    df_timeprofile2['emissions'].plot(ax=ax2, color='r', label='5 PM')
    df_timeprofile3['emissions'].plot(ax=ax2, color='g', label='6 PM')
    ax2.set_title('Emissions')
    ax2.set(xlabel="Date of Departure", ylabel="CO2 Emissions (kg)")

    df_timeprofile['distance'].plot(ax=ax3, label="10 AM")
    df_timeprofile2['distance'].plot(ax=ax3, color='r', label='5 PM')
    df_timeprofile3['distance'].plot(ax=ax3, color='g', label='6 PM')
    ax3.set_title('Distance')
    ax3.set(xlabel="Date of Departure", ylabel="Travel Distance (km)")

    plt.legend(loc='best')
    plt.show()


if __name__ == '__main__':
   #timeProfileLoop("2020-06-28 17:00", timestep=1440, days=7)
   plotTimeProfile('output/timeprofile_20200625T1648.csv', 'output/timeprofile_20200628t0927.csv', 'output/timeprofile_20200625T1642.csv')