# Get-Pull-Points
This python script takes a polygon and returns n equally space points inside the the polygon. 

The script helps to overcome some of the page limits / request limits associated with various location based apis. For example, suppose you want to pull all of the bars from the Google Place API in a particular city. Google however only lets you pull the first 60 results of your criteria. If you want to pull more results than that, you need a quick and efficient way to split your territory up into n segments (depending on the size). This script does exactly that.

The script also lets you plot the new points on a map.

Requires:
OSMNX 
Geopandas
Numpy
