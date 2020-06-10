import pandas as pd
import os


# create a sample dataFrame with speeds per segment

#speedPerSegmentDict = {'segment': [0, 1, 2, 3, 4],
                       #'Speed': [9, 70, 55, 80, 70]}

#speedPerSegmentDF = pd.DataFrame(speedPerSegmentDict)
#speedPerSegmentDF.to_csv('data/b_SpeedFlow_sample.csv')

# this function derive values for further emission factors calculation
def derive_values_for_calc(path_input_emis_calc, category, fuel, segment, fuel_st, technology, pollutant):
    values_for_emis_calc = pd.read_csv(path_input_emis_calc)
    df_values = values_for_emis_calc[(values_for_emis_calc['Category'] == category) &
                                     (values_for_emis_calc['Fuel'] == fuel) &
                                     (values_for_emis_calc['Segment'] == segment) &
                                     (values_for_emis_calc['Euro Standard'] == fuel_st) &
                                     (values_for_emis_calc['Technology'] == technology) &
                                     (values_for_emis_calc['Pollutant'] == pollutant)]
    return df_values['Alpha'], df_values['Beta'], df_values['Gamma'], df_values['Delta'], df_values['Epsilon'], df_values['Zita'], df_values['Hta']


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
        elif speed > 130.00:
            speed = 130.00
        else:
            speed = speed_per_seg.loc[i, 'Speed']
        emis_f = formula_emission_factor(a, b, g, d, e, z, h, speed)
        emis_fs += [emis_f]
    emis_per_seg = pd.DataFrame(emis_fs)
    if os.path.exists('../data/c02_emisFactor_perSeg_perCar.csv'):
        return emis_per_seg
    else:
        emis_per_seg.to_csv('../data/c02_emisFactor_perSeg_perCar.csv')
    return emis_per_seg


# input to check the result
result = calculate_emission_factor('../data/Ps_STEEP_a_emis.csv', 'Passenger Cars', 'Petrol', 'Mini', 'Euro 4', 'GDI',
                                   'EC', '../data/b_SpeedFlow_sample.csv')
print(result)