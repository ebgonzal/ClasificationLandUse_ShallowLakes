# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 10:46:22 2021

@author: Belen
"""

#paquetes
from osgeo import gdal
import numpy as np
import os
import fiona
import os, fnmatch
import geopandas as gpd


########################################################################
#1 Calcular un area de 2.5 km alrededor cada laguna. Los archivos de las 
#los archivos shp de  lagunas estan en una carpeta dentro de este repositorio

# path de la carpeta donde estan los shp
folder_path = "C:/Users.../shplagunas"

#lista de los archivos shp
shapefiles = [file for file in os.listdir(folder_path) if file.endswith('.shp')]

# loop para cortar 2.5 km aldedor de cada laguna
for shapefile in shapefiles:    
    shapefile_path = os.path.join(folder_path, shapefile)        
    lakes = gpd.read_file(shapefile_path)
    lakes_buffer = lakes.buffer(2500)
    lakes_buffer_gdf = gpd.GeoDataFrame(geometry=lakes_buffer)    
    output_path = os.path.join(folder_path, shapefile.replace('.shp', '_buffer.shp'))
    
    # Se guardan los resultados
    lakes_buffer_gdf.to_file(output_path)

###############################################################################
#2-Cortar las imagenes con los buffer de 2.5 calculados arriba 

#setear el clip a usar, y las carpetas de entrada y salida
CLIP= 'C:/Users/..._buffer.shp'
INPUT_FOLDER='C:/Users/Desktop/..'
OUTPUT= 'C:/Users/Desktop/..'

def findRasters (path, filter):
    for root, dirs, files in os.walk(path):
        for file in fnmatch.filter(files, filter):
            yield file
#loop para cortar y se guardan con el mismo nombre+clip
for raster in findRasters(INPUT_FOLDER, '*.tif'):
    inRaster = INPUT_FOLDER + '/' + raster
    outRaster = OUTPUT + '/clip_' + raster
    cmd = 'gdalwarp -q -cutline %s -crop_to_cutline %s %s' % (CLIP, inRaster, outRaster)
    os.system(cmd)


