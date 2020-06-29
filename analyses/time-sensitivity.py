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


def plotWeekTimeProfile(file1, t1, file2, t2,  file3, t3):
    """ Function to plot weekly sensitivity against eachother.
        - file1, file2, file3, [.csv]: result of timeProfileLoop function, in which the timestep was set for 1440
        - t1, t2, t3, [string]; the time for which each respective time profile was conducted """

    # Read from csv file into pandas dataframe
    df_timeprofile = pd.read_csv(file1, index_col=0, parse_dates=True)
    df_timeprofile['time'] = df_timeprofile['time']/60
    df_timeprofile['distance'] = df_timeprofile['distance']/1000
    df_timeprofile2 = pd.read_csv(file2, index_col=0, parse_dates=True)
    df_timeprofile2['time'] = df_timeprofile2['time'] / 60
    df_timeprofile2['distance'] = df_timeprofile2['distance'] / 1000
    df_timeprofile3 = pd.read_csv(file3, index_col=0, parse_dates=True)
    df_timeprofile3['time'] = df_timeprofile3['time'] / 60
    df_timeprofile3['distance'] = df_timeprofile3['distance'] / 1000
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)

    df_timeprofile['time'].plot(ax=ax1, label=t1)
    df_timeprofile2['time'].plot(ax=ax1, color='r', label=t2)
    df_timeprofile3['time'].plot(ax=ax1, color='g', label=t3)
    ax1.set_title('Time')
    ax1.set(xlabel="Date of Departure", ylabel="Travel Time (min)")

    df_timeprofile['emissions'].plot(ax=ax2, label=t1)
    df_timeprofile2['emissions'].plot(ax=ax2, color='r', label=t2)
    df_timeprofile3['emissions'].plot(ax=ax2, color='g', label=t3)
    ax2.set_title('Emissions')
    ax2.set(xlabel="Date of Departure", ylabel="CO2 Emissions (kg)")

    df_timeprofile['distance'].plot(ax=ax3, label=t1)
    df_timeprofile2['distance'].plot(ax=ax3, color='r', label=t2)
    df_timeprofile3['distance'].plot(ax=ax3, color='g', label=t3)
    ax3.set_title('Distance')
    ax3.set(xlabel="Date of Departure", ylabel="Travel Distance (km)")

    plt.legend(loc='best')
    fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.2)
    fig.set_figheight(6)
    fig.set_figwidth(16)
    plt.savefig('output/d02_sensitiv_routing_week_plot.pdf')

def plotDailyTimeProfile(file1, int1, file2, int2):
        """ Function to plot weekly sensitivity against eachother.
            - file1, file2, [.csv]: result of timeProfileLoop function for a single day
            - int1, int2, [string]; the time interval for which each respective time profile was conducted """

        # Read from csv file into pandas dataframe
        df_timeprofile = pd.read_csv(file1, index_col=0, parse_dates=True)
        df_timeprofile['time'] = df_timeprofile['time'] / 60
        df_timeprofile['distance'] = df_timeprofile['distance'] / 1000

        df_timeprofile2 = pd.read_csv(file2, index_col=0, parse_dates=True)
        df_timeprofile2['time'] = df_timeprofile2['time'] / 60
        df_timeprofile2['distance'] = df_timeprofile2['distance'] / 1000

        fig, (ax1, ax2, ax3) = plt.subplots(1, 3)

        df_timeprofile['time'].plot(ax=ax1, label=int1)
        df_timeprofile2['time'].plot(ax=ax1, color='r', label=int2)
        ax1.set_title('Time')
        ax1.set(xlabel="Time of Departure", ylabel="Travel Time (min)")

        df_timeprofile['emissions'].plot(ax=ax2, label=int1)
        df_timeprofile2['emissions'].plot(ax=ax2, color='r', label=int2)
        ax2.set_title('Emissions')
        ax2.set(xlabel="Time of Departure", ylabel="CO2 Emissions (kg)")

        df_timeprofile['distance'].plot(ax=ax3, label=int1)
        df_timeprofile2['distance'].plot(ax=ax3, color='r', label=int2)
        ax3.set_title('Distance')
        ax3.set(xlabel="Time of Departure", ylabel="Travel Distance (km)")

        plt.legend(loc='best')
        fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.2)
        fig.set_figheight(6)
        fig.set_figwidth(16)
        plt.savefig('output/d02_sensitiv_routing_daily_plot.pdf')


if __name__ == '__main__':
    #timeProfileLoop("2020-06-28 17:00", timestep=1440, days=7) # uncomment to create custom time profiles
    plotWeekTimeProfile('output/d02_sensitiv_routing_timeprofile_10AM.csv','10 AM', 'output/d02_sensitiv_routing_timeprofile_5PM.csv', '5 PM', 'output/d02_sensitiv_routing_timeprofile_6PM.csv', '6 PM')
    plotDailyTimeProfile('output/d02_sensitiv_routing_timeprofile_10min.csv', '10 min', 'output/d02_sensitiv_routing_timeprofile_60min.csv', '60 min')