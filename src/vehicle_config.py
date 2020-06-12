""" vehicle_config.py

    Defines vehicle parameter options for the COPERT+ Model

"""

class VehicleConfig:
    """Defines vehicle parameter options for the COPERT+ Model"""

    def __init__(self):
        """Constructor"""
        self.fuels = ['Petrol', 'Diesel', 'Petrol Hybrid', 'LPG Bifuel ~ LPG', 'LPG Bifuel ~ Petrol', 'CNG Bifuel ~ Petrol', 'CNG Bifuel ~ CNG']
        self.segments = ['Mini', 'Small', 'Medium', 'Large-SUV-Executive', '2-Stroke']
        self.standards = ['Conventional', 'ECE 15/00-01', 'ECE 15/02', 'ECE 15/03', 'ECE 15/04', 'Euro 1', 'Euro 2', 'Euro 3', 'Euro 4',\
                'Euro 5', 'Euro 6', 'Euro 6 2017-2019', 'Euro 6 2020+', 'Euro 6 up to 2016', 'Improved Conventional', 'Open Loop', 'PRE ECE']