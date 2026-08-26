import rasterio
import geopandas
import shapely
import pyproj
import numpy
import scipy
import xarray
import rioxarray
import cv2

print("================================")
print("   GIS ENVIRONMENT TEST")
print("================================")

print("Rasterio :", rasterio.__version__)
print("GeoPandas:", geopandas.__version__)
print("Shapely  :", shapely.__version__)
print("PyProj   :", pyproj.__version__)
print("NumPy    :", numpy.__version__)
print("SciPy    :", scipy.__version__)
print("Xarray   :", xarray.__version__)
print("rioxarray:", rioxarray.__version__)
print("OpenCV   :", cv2.__version__)

print("================================")
print("GIS ENVIRONMENT WORKING!")
print("================================")