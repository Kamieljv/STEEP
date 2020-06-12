""" emissions.py

    Required packages:
    - pandas
    - os

    The class(es) in this document are loaded by 'app.py'.
    This emission calculator is based on the COPERT+ model (https://www.emisia.com/utilities/copert/)

"""

import pandas as pd

class EmissionCalculator:
    """Derives values for further emission factors calculation"""

    def __init__(self, modelpath, fuel="Petrol", segment="Medium", standard="Euro 6 2017-2019", technology="GDI", pollutant="EC"):
        """ Initializes the class
            - modelpath [string]: absolute/relative path to the emission model sheet (as .csv)
            - fuel [string]*
            - segment [string]*
            - standard [string]*
            - technology [string]*
            - pollutant [string]*
            (* Options for this variable are specified in src/vehicle_config.py.)
        """
        self.modelpath = modelpath
        self.fuel = fuel
        self.segment = segment
        self.standard = standard
        self.technology = technology
        self.pollutant = pollutant

    def get_parameters(self):
        """ Retrieves the parameters from the emission model file based on vehicle characteristics."""
        values_for_emis_calc = pd.read_csv(self.modelpath)
        df_values = values_for_emis_calc[(values_for_emis_calc['Fuel'] == self.fuel) &
                                         (values_for_emis_calc['Segment'] == self.segment) &
                                         (values_for_emis_calc['Euro Standard'] == self.standard) &
                                         (values_for_emis_calc['Technology'] == self.technology) &
                                         (values_for_emis_calc['Pollutant'] == self.pollutant)]
        return df_values['Alpha'], df_values['Beta'], df_values['Gamma'], df_values['Delta'], df_values['Epsilon'], df_values['Zita'], df_values['Hta']

    def emission_formula(self, speed):
        """ Computes the emission factor based on model input parameters. """
        return (self.a * speed ** 2 + self.b * speed + self.g + (self.d / speed)) / \
               (self.e * speed ** 2 + self.z * speed + self.h)

    def calculate_emission_factor(self, route, minspeed=10, maxspeed=130):
        """ Calculates the emission factors for a set of roads
            - route [GeoPandas GeoDataFrame]: the route with speed column
            - minspeed [int]: the minimum speed to calculate emissions for, all speeds below are set to this value
            - maxspeed [int]: the maximum speed to calculate emissions for, all speeds above are set to this value
         """

        self.a, self.b, self.g, self.d, self.e, self.z, self.h = self.get_parameters()

        # Apply speed mask of minspeed <= speed <= maxspeed
        route.loc[route['speed'] < minspeed, 'speed'] = minspeed
        route.loc[route['speed'] > maxspeed, 'speed'] = maxspeed

        route['em_fac'] = route.apply(lambda row: self.emission_formula(row.speed), axis=1)
        self.route = route

        return route

    def calculate_stats(self):
        """ Calculates the route emissions (gCO2) based on the emission factors and segment lengths """

        self.route['emissions'] = self.route.apply(lambda row: (row.distance / 1000) * row.em_fac, axis=1)

        return self.route['emissions'].sum(), int(self.route['distance'].sum()), int(self.route['time'].sum())