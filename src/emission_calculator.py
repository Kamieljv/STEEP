""" emissions.py

    Required packages:
    - pandas
    - os

    The class(es) in this document are loaded by 'app.py'.
    This emission calculator is based on the COPERT+ model (https://www.emisia.com/utilities/copert/)
    The conversion values are based on RVO CO2 fuel emission factors (https://english.rvo.nl/sites/default/files/2019/05/The%20Netherlands%20list%20of%20fuels%20version%20January%202019.pdf)

"""

import pandas as pd

class EmissionCalculator:
    """Derives values for further emission factors calculation"""

    def __init__(self, modelpath, conversionpath, fuel="Petrol", segment="Medium", standard="Euro 6 2017-2019", technology="GDI", pollutant="EC"):
        """ Initializes the class
            - modelpath [string]: absolute/relative path to the emission model sheet (as .csv)
            - conversionpath [string]: absolute/relative path to the conversion factors sheet (as .csv)
            - fuel [string]*
            - segment [string]*
            - standard [string]*
            - technology [string]*
            - pollutant [string]*
        """
        self.modelpath = modelpath
        self.df_conversion = pd.read_csv(conversionpath)
        self.fuel = fuel
        self.segment = segment
        self.standard = standard
        self.technology = technology
        self.pollutant = pollutant
        self.CO2conv = self.CO2_conversion() #in kg/MJ

    def get_parameters(self):
        """ Retrieves the parameters from the emission model file based on vehicle characteristics."""
        values_for_emis_calc = pd.read_csv(self.modelpath)
        df_values = values_for_emis_calc[(values_for_emis_calc['Fuel'] == self.fuel) &
                                         (values_for_emis_calc['Segment'] == self.segment) &
                                         (values_for_emis_calc['Euro Standard'] == self.standard) &
                                         # (values_for_emis_calc['Technology'] == self.technology) &
                                         (values_for_emis_calc['Pollutant'] == self.pollutant)]
        # Take the first row if multiple exist
        df_values = df_values.iloc[0]
        return df_values['Alpha'], df_values['Beta'], df_values['Gamma'], df_values['Delta'], df_values['Epsilon'], df_values['Zita'], df_values['Hta']

    def get_options(self, choice):
        """ Retrieves the vehicle parameter options based on a user's initial choice.
            - choice [dict]: contains a vehicle parameter choice if set by user
        """
        # List the dict keys for later use
        inputs = [k for k, v in choice.items()]
        # Filter out keys with empty values
        choice = {k: v for k, v in choice.items() if v}
        # Get all options from COPERT model sheet
        options = pd.read_csv(self.modelpath)

        # Translate dict keys to csv columns
        col = {'fuel':'Fuel', 'segment':'Segment', 'standard':'Euro Standard'}

        # Filter options based on choices
        for k, v in choice.items():
            options = options[options[col[k]] == v]

        options_dict = dict()
        for var in inputs:
            options_dict[var] = list(options[col[var]].unique())

        return options_dict


    def ec_formula(self, speed):
        """ Computes the emission factor based on model input parameters. """
        return (self.a * speed ** 2 + self.b * speed + self.g + (self.d / speed)) / \
               (self.e * speed ** 2 + self.z * speed + self.h)

    def CO2_conversion(self):
        """ Retrieves the conversion factor based on fuel type of vehicle."""
        conv_value = self.df_conversion[(self.df_conversion['Fuel'] == self.fuel)]
        return (conv_value["CO2 EF kg/MJ"])


    def calculate_ec_factor(self, route, minspeed=10, maxspeed=130):
        """ Calculates the EC emission factors for a set of roads
            - route [GeoPandas GeoDataFrame]: the route with speed column
            - minspeed [int]: the minimum speed to calculate emissions for, all speeds below are set to this value
            - maxspeed [int]: the maximum speed to calculate emissions for, all speeds above are set to this value
         """

        self.a, self.b, self.g, self.d, self.e, self.z, self.h = self.get_parameters()

        # Apply speed mask of minspeed <= speed <= maxspeed
        route.loc[route['speed'] < minspeed, 'speed'] = minspeed
        route.loc[route['speed'] > maxspeed, 'speed'] = maxspeed

        route['ec_fac'] = route.apply(lambda row: self.ec_formula(row.speed), axis=1)
        route['co2_fac'] = route.apply(lambda row: self.CO2conv * row["ec_fac"])
        self.route = route

        return route

    def calculate_stats(self):
        """ Calculates the route emissions (kgCO2) based on the emission factors and segment lengths """

        self.route['emissions'] = self.route.apply(lambda row: (row.distance / 1000) * row.em_fac, axis=1)

        return self.route['emissions'].sum(), int(self.route['distance'].sum()), int(self.route['time'].sum())
