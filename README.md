# STEEP (by Team Inselberg*)
> STEEP: A SpatioTemporal Emission Estimator for Passenger vehicles

_*Team Inselberg: Verónica Arambula Coyote, Alena Izotova, Elina Kreuzberg, HuanHuan Li, Kamiel Verhelst; all students of the Master Geo-Information Science at Wageningen University, The Netherlands._

STEEP is a model that estimates the CO2 emissions of passenger cars on a specific route, at a specific time of departure.
The model combines a time-dependent routing algorithm ([TomTom's Routing API](https://developer.tomtom.com/routing-api/routing-api-documentation)) 
with a vehicle emission model ([COPERT+](https://www.emisia.com/utilities/copert/)). 

This repository contains the main model code, wrapped in a web-based user interface based on Python. 

## Installation
To run the application, a set of Python and geo packages need to be installed. We recommend using [Conda](https://docs.conda.io/en/latest/) as a package manager.
With Conda, create a virtual environment using the `environment.yml` provided. 

Create the Conda environment using: `conda env create -f environment.yml`.

In case packages are not available in the specified channels, they can be searched for on https://anaconda.org/ and manually installed. 

## Usage

### Set your TomTom API Key
If you do not have an active TomTom API key, you can get it [here](https://developer.tomtom.com/user/register).
Fill in the API key in `src/routing.py` on line 27.

### Running STEEP
To run STEEP, open a terminal and head to this repository, or open the repository in your favourite text editor. 
Then run the app (terminal: `python app.py`).