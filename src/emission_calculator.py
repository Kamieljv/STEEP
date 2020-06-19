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
                                         # (values_for_emis_calc['Technology'] == self.technology) &
                                         (values_for_emis_calc['Pollutant'] == self.pollutant)]
        # Take the first row if multiple exist
        df_values = df_values.iloc[0]
        return df_values['Alpha'], df_values['Beta'], df_values['Gamma'], df_values['Delta'], df_values['Epsilon'], df_values['Zita'], df_values['Hta']

    def get_options(self, choice=None):
        """ Retrieves the vehicle parameter options based on a user's initial choice.
            - choice [dict]: contains a vehicle parameter choice if set by user
        """
        if choice != None:
            # List the dict keys for later use
            inputs = [k for k, v in choice.items()]
            # Filter out keys with empty values
            choice = {k: v for k, v in choice.items() if v}

        # Get all options from COPERT model sheet
        options = pd.read_csv(self.modelpath)

        # Translate dict keys to csv columns
        col = {'fuel':'Fuel', 'segment':'Segment', 'standard':'Euro Standard'}

        # Filter options based on choices
        if choice != None:
            for k, v in choice.items():
                options = options[options[col[k]] == v]
        else:
            inputs = [k for k, v in col.items()]

        options_dict = dict()
        for var in inputs:
            options_dict[var] = list(options[col[var]].unique())

        return options_dict


    def emission_formula(self, speed):
        """ Computes the emission factor based on model input parameters. """
        return (self.a * speed ** 2 + self.b * speed + self.g + (self.d / speed)) / \
               (self.e * speed ** 2 + self.z * speed + self.h)

    def calculate_emission_factor(self, route, minspeed=10, maxspeed=130):
        """ Calculates the emission factors for a set of roads
            - route [pandas/Geopandas dataframe]: the route with 'speed' column
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

        return round(self.route['emissions'].sum(),3), int(self.route['distance'].sum()), int(self.route['time'].sum())
