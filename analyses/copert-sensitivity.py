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

# Configuration from COPERT
min_speed = 10
max_speed = 130

options = EmissionCalculator('../data/Ps_STEEP_a_emis.csv').get_options()

def plotFuelOptions():
    fig = plt.figure()
    for fuel in options['fuel']:
        # Initialize calculator with COPERT model file
        calculator = EmissionCalculator('../data/Ps_STEEP_a_emis.csv',
                                        fuel=fuel,
                                        segment="Small",
                                        standard="Euro 5",
                                        pollutant="EC")



        df_speed = pd.DataFrame({'speed': np.linspace(min_speed, max_speed, 100)})

        df_emfac = calculator.calculate_emission_factor(df_speed)

        plt.plot('speed', 'em_fac', data=df_emfac, label=fuel)

    plt.legend()
    plt.title('Emission factors per speeds of different fuel types')
    plt.xlabel('Emission factor (gCO2/km)')
    plt.ylabel('Speed (km/hr)')
    plt.show()



if __name__ == '__main__':
    plotFuelOptions()

