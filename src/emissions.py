import pandas as pd
import numpy as np
import geojson
import os
os.chdir('C:/Data/ACT_GIS/STEEP/')

##required inputs: Car_parameters (as dictionary), segment speed(as a value)
##outputs of emmissionfactor fuction will be a g/km value which can be used to calculate the emissions of a segment
emmisions = pd.read_csv('data/EC_Factors_Passenger.csv')
#with open("static\TestRoute_Wag_Roest.geojson") as gj_file:
  #  gj = geojson.load(gj_file)
#speeds = []
#for feature in gj['features']:
 #   print(feature['attributes'])

#route =
#speed = sample.geojson[]
print(emmisions.head())

