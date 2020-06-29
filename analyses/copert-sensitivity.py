""" copert-sensitivity.py

    Required packages:
    - pandas
    - numpy
    - matplotlib.pyplot

    Usage:

    This script is meant to run independently.

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.emission_calculator import EmissionCalculator


def plotEmFacProfile(ax, parameter='fuel', min_speed=10, max_speed=130):

    # Set defaults; clear value for chosen parameter
    defaults = {'fuel':"Petrol", 'segment':"Small", 'standard':"Euro 6 2017-2019"}
    defaults[parameter] = ""

    # Get the possible options
    options = EmissionCalculator(root="../").get_options(defaults)

    for var in options[parameter]:
        # do not plot 'LPG Bifuel ~ Petrol' or 'CNG Bifuel ~ Petrol' because they are identical to 'Petrol'
        if parameter == 'fuel' and var in ['LPG Bifuel ~ Petrol', 'CNG Bifuel ~ Petrol']:
            continue
        if parameter == 'standard' and var not in ['Euro 4', 'Euro 5', 'Euro 6 up to 2016', 'Euro 6 2017-2019', 'Euro 6 2020+']:
            continue

        defaults[parameter] = var

        # Initialize calculator with vehicle parameters
        calculator = EmissionCalculator(fuel=defaults['fuel'],
                                        segment=defaults['segment'],
                                        standard=defaults['standard'], root="../")



        df_speed = pd.DataFrame({'speed': np.linspace(min_speed, max_speed, 100)})

        df_co2fac = calculator.calculate_ec_factor(df_speed)

        ax.plot('speed', 'co2_fac', data=df_co2fac, label=var)

    ax.legend()
    ax.set_title(parameter.capitalize() + 's')
    ax.set(xlabel='Speed (km/h)', ylabel='Emission factor (kgCO2/km)')

    return df_co2fac

def plotMultipleProfiles(outdir, fbase):
    fig, axs = plt.subplots(1, 3)
    fig.set_figheight(5)
    fig.set_figwidth(16)
    fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.2)

    df_profiles = pd.DataFrame()
    for i, param in enumerate(['fuel', 'segment', 'standard']):
        df_profile = plotEmFacProfile(axs[i], param)
        df_profiles['speed'], df_profiles['ec_fac_'+param], df_profiles['co2_fac_'+param] = df_profile['speed'], df_profile['ec_fac'], df_profile['co2_fac']

    plt.savefig(outdir + fbase + 'plot.pdf')
    df_profiles.to_csv(outdir + fbase + 'data.csv')


if __name__ == '__main__':
    plotMultipleProfiles(outdir='output/', fbase='d01_sensitiv_copert_')