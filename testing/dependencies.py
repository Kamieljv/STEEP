""" dependencies.py

    Usage:
    This script lists the dependencies used in this project and imports them for testing purposes.
    This script is meant to run independently.

"""

# First import packages needed for listing and importing other packages
print("Importing required packages for testing...")
from findimports import find_imports_and_track_names
import importlib, os

# Create a list of python files
print("Listing Python files in project...")
files = []
for (dirpath, dirnames, filenames) in os.walk(os.getcwd()):
    for file in filenames:
        if file[-3:] == ".py":
            files.append(os.path.join(dirpath, file))

print("Listing imports in project's Python files...")
dependencies = []
for file in files:
    imports, unused_names = find_imports_and_track_names(file)
    for i in imports:
        dependencies.append(i.name)

print("Loading project packages...")
for dep in dependencies:
    name = dep.split('.')[0]
    importlib.import_module(name)

print("Test Successful. Required packages installed and functional.")