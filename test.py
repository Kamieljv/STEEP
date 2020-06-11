import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
data = {'name': ['a', 'b', 'c'],
        'x': [173994.1578792833, 173974.1578792833, 173910.1578792833],
        'y': [444135.6032947102, 444186.6032947102, 444111.6032947102]}
df = pd.DataFrame(data)
print(df.head)
geometry = [Point(xy) for xy in zip(df['x'], df['y'])]
wageningenGDF = gpd.GeoDataFrame(df, geometry=geometry)
wageningenGDF.crs = {'init': 'epsg:28992'}
wageningenGDF.plot(marker='*', color='green', markersize=50)
print(type(wageningenGDF), len(wageningenGDF))

