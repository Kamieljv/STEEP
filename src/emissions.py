import pandas as pd
import numpy as np
# import geojson
import os

# os.chdir('C:/Data/ACT_GIS/STEEP/') # for Eli
os.chdir('/home/alena/my_project/STEEP/')  # for Alena

##required inputs: Car_parameters (as dictionary), segment speed(as a value)
##outputs of emissionfactor fuction will be a g/km value which can be used to calculate the emissions of a segment
# emissions = pd.read_csv('data/EC_Factors_Passenger.csv')
# with open("static\TestRoute_Wag_Roest.geojson") as gj_file:
#  gj = geojson.load(gj_file)
# speeds = []
# for feature in gj['features']:
#   print(feature['attributes'])

# route =
# speed = sample.geojson[]
# print(emissions.head())

# final formula (Alpha * Speed ^ 2 + Beta * Speed + Gamma + (Delta/Speed) ) / (Epsilon * Speed^2 + Zita * Speed + Hta)

# input will be speeds for each segment in csv
# path is a path to the file
# def constructSpeedDF (path):
# spDF = read_csv(str(path))

# create a sample dataFrame with speeds per segment

speedPerSegmentDict = {'segment': [0, 1, 2, 3, 4],
                       'Speed': [9, 70, 55, 80, 70]}

speedPerSegmentDF = pd.DataFrame(speedPerSegmentDict)
speedPerSegmentDF.to_csv('data/b_SpeedFlow_sample.csv')

# this function derive values for further emission factors calculation
def derive_values_for_calc(path_input_emis_calc, category, fuel, segment, fuel_st, technology, pollutant):
    # maybe we should check that all the inputs are strings before make df
    values_for_emis_calc = pd.read_csv(path_input_emis_calc)
    df_values = values_for_emis_calc[(values_for_emis_calc['Category'] == category) &
                                     (values_for_emis_calc['Fuel'] == fuel) &
                                     (values_for_emis_calc['Segment'] == segment) &
                                     (values_for_emis_calc['Euro Standard'] == fuel_st) &
                                     (values_for_emis_calc['Technology'] == technology) &
                                     (values_for_emis_calc['Pollutant'] == pollutant)]
    a = df_values['Alpha']
    b = df_values['Beta']
    g = df_values['Gamma']
    d = df_values['Delta']
    e = df_values['Epsilon']
    z = df_values['Zita']
    h = df_values['Hta']
    return a, b, g, d, e, z, h


# This a separate function for formula
def formula_emission_factor(a, b, g, d, e, z, h, speed):
    emis_f = a * speed ** 2 + b * speed + g + (d / speed) / (e * speed ** 2 + z * speed + h)
    return emis_f


# Unite two previous functions into one, where output is the dataframe with emission factor per segment
def calculate_emission_factor(path_input_emis_calc, category, fuel, segment, fuel_st, technology, pollutant,
                              path_speeds_per_seg):
    a, b, g, d, e, z, h = derive_values_for_calc(path_input_emis_calc, category, fuel, segment, fuel_st, technology,
                                                 pollutant)
    speed_per_seg = pd.read_csv(path_speeds_per_seg, index_col='segment')
    speed_per_seg.drop(columns=['Unnamed: 0'])
    emis_fs = []
    for i in range(speed_per_seg.index.size):
        speed = speed_per_seg.loc[i, 'Speed']
        if speed < 10.00:
            speed = 10.00
            emis_f = formula_emission_factor(a, b, g, d, e, z, h, speed)
        elif speed > 130.00:
            speed = 130.00
            emis_f = formula_emission_factor(a, b, g, d, e, z, h, speed)
        else:
            speed = speed_per_seg.loc[i, 'Speed']
            emis_f = formula_emission_factor(a, b, g, d, e, z, h, speed)

        emis_fs += [emis_f]
    emis_per_seg = pd.DataFrame(emis_fs)
    emis_per_seg.to_csv('data/c02_emisFactor_perSeg_perCar.csv')
    return emis_per_seg


# input to check the result
result = calculate_emission_factor('data/Ps_STEEP_a_emis.csv', 'Passenger Cars', 'Petrol', 'Mini', 'Euro 4', 'GDI',
                                   'EC', 'data/b_SpeedFlow_sample.csv')
print(result)