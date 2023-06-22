# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 14:41:08 2022

@author: Belen
"""
#https://sentinelsat.readthedocs.io/en/stable/

#se instala sentinel sat en anaconda prompt con:  pip install sentinelsat 

from sentinelsat import SentinelAPI
from sentinelsat import read_geojson
from sentinelsat import geojson_to_wkt
from datetime import datetime

# conectar con la API usando usuario y contraseña de copernicus hub
api = SentinelAPI('usuario', 'contraseña', 'https://apihub.copernicus.eu/apihub')


#fechas de inicio y fin de la búsqueda
date_start_search = datetime.strptime("2010-07-17","%Y-%m-%d")
print(date_start_search)
date_end_search = datetime.strptime("2022-07-18","%Y-%m-%d")
print(date_end_search)


# el map.geojson se guarda en ese formato acá https://geojson.io/#map=2/20.0/0.0
footprint = geojson_to_wkt(read_geojson('map.geojson')) 
products = api.query(footprint,
                     #producttype='S2MSI2A',
                     #orbitdirection='ASCENDING',
                     date = (date_start_search, date_end_search),
                     platformname = 'Sentinel-2',
                     processinglevel = 'Level-2A',
                     cloudcoverpercentage = (0, 90),
                     limit=3)#limite de imagenes

print(len(products))

#descarga las imagenes    
api.download_all(products)
