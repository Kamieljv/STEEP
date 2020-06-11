""" emissions.py

    Required packages:
    - pandas
    - os

    The class(es) in this document are loaded by 'app.py'.
    This emission calculator is based on the COPERT+ model (https://www.emisia.com/utilities/copert/)

"""

class EmissionCalculator:
    """Derives values for further emission factors calculation"""

    def __init__(self, modelpath, fuel="Petrol", segment="Medium", standard="Euro 6", technology="GDI", pollutant="EC"):
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

    def apply_formula(self, a, b, g, d, e, z, h, speed):
        """ Computes the emission factor based on model input parameters. """
        return (a * speed ** 2 + b * speed + g + (d / speed)) / (e * speed ** 2 + z * speed + h)

    def calculate_emission_factor(self):
        a, b, g, d, e, z, h = self.get_parameters(self)
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
            emis_f = apply_formula(a, b, g, d, e, z, h, speed)
            emis_fs += [emis_f]
        emis_per_seg = pd.DataFrame(emis_fs)

        return emis_per_seg