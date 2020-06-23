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
    options = EmissionCalculator('../data/Ps_STEEP_a_emis.csv').get_options(defaults)

    for var in options[parameter]:
        # do not plot 'LPG Bifuel ~ Petrol' or 'CNG Bifuel ~ Petrol' because they are identical to 'Petrol'
        if var in ['LPG Bifuel ~ Petrol', 'CNG Bifuel ~ Petrol']:
            continue

        defaults[parameter] = var

        # Initialize calculator with COPERT model file
        calculator = EmissionCalculator('../data/Ps_STEEP_a_emis.csv',
                                        fuel=defaults['fuel'],
                                        segment=defaults['segment'],
                                        standard=defaults['standard'])



        df_speed = pd.DataFrame({'speed': np.linspace(min_speed, max_speed, 100)})

        df_emfac = calculator.calculate_emission_factor(df_speed)

        ax.plot('speed', 'em_fac', data=df_emfac, label=var)

    ax.legend()
    ax.set_title(parameter.capitalize() + 's')
    ax.set(xlabel='Speed (km/h)', ylabel='Emission factor (kgCO2/km)')

def plotMultipleProfiles():
    fig, axs = plt.subplots(1, 3)

    for i, param in enumerate(['fuel', 'segment', 'standard']):
        plotEmFacProfile(axs[i], param)

    plt.show()



if __name__ == '__main__':
    plotMultipleProfiles()

