import pandas as pd
import numpy as np
import geojson
import os
# os.chdir('C:/Data/ACT_GIS/STEEP/') # for Eli
os.chdir('/home/alena/my_project/STEEP/') # for Alena

##required inputs: Car_parameters (as dictionary), segment speed(as a value)
##outputs of emissionfactor fuction will be a g/km value which can be used to calculate the emissions of a segment
#emissions = pd.read_csv('data/EC_Factors_Passenger.csv')
#with open("static\TestRoute_Wag_Roest.geojson") as gj_file:
  #  gj = geojson.load(gj_file)
#speeds = []
#for feature in gj['features']:
 #   print(feature['attributes'])

#route =
#speed = sample.geojson[]
# print(emissions.head())

#final formula (Alpha * Speed ^ 2 + Beta * Speed + Gamma + (Delta/Speed) ) / (Epsilon * Speed^2 + Zita * Speed + Hta)

#input will be speeds for each segment in csv
#path is a path to the file
#def constructSpeedDF (path):
#spDF = read_csv(str(path))

# create a sample dataFrame with speeds per segment
# this is just to be able to check if all the functions are working
speedPerSegmentDict = {'segment': [1, 2, 3, 4, 5],
         'MaxSpeed': [60, 70, 55, 80, 70],
         'MinSpeed': [0, 60, 40, 50, 0]}

speedPerSegmentDF = pd.DataFrame(speedPerSegmentDict)
speedPerSegmentDF.to_csv('sample_speed_per_segment.csv', sep = '\t')

def deriveValues(path_values, category, fuel, segment, fuel_st, technology, pollutant):
    # maybe we should check that all the inputs are strings before make df
    valuesDF = pd.read_csv(path_values)
    dfForCalculation = valuesDF[(valuesDF['Category'] == category) & (valuesDF['Fuel'] == fuel) & (valuesDF['Segment'] == segment) &
                                (valuesDF['Euro Standard'] == fuel_st) & (valuesDF ['Technology'] == technology) & (valuesDF['Pollutant'] == pollutant)]
    a = dfForCalculation['Alpha']
    b = dfForCalculation['Beta']
    g = dfForCalculation['Gamma']
    d = dfForCalculation['Delta']
    e = dfForCalculation['Epsilon']
    z = dfForCalculation['Zita']
    h = dfForCalculation['Hta']
    return a, b, g, d, e, z, h

def calculateReductionFactor (path_values, category, fuel, segment, fuel_st, technology, pollutant, path_speeds_per_segm):
    a, b, g, d, e, z, h = deriveValues(path_values, category, fuel, segment, fuel_st, technology, pollutant)
    speedPerSegm = pd.read_csv('path_speeds_per_segm')
    # add formula (Alpha * Speed ^ 2 + Beta * Speed + Gamma + (Delta / Speed)) / (Epsilon * Speed ^ 2 + Zita * Speed + Hta)
    # make a df with reductionFactor per segment reductFPerSeg =
    return reductFPerSeg
