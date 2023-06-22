# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 14:37:24 2021

@author: Belen
"""
#load package
from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
import os
from osgeo import gdal, gdal_array
from sklearn import cluster

###########################################################################
#abrir los raster clip
img_ds = gdal.Open('C:/Users/..clip_laguna.tif')

#para visualizar 1 sola banda 
array = img.GetRasterBand(1).ReadAsArray()
plt.figure()
plt.imshow(array)
plt.colorbar()
plt.show()


###########################################################################
#Clasificación no supervisada K-means

#para abrir la imagen multibanda se inicia un array de ceros con la data de la imagen
#original
img = np.zeros((img_ds.RasterYSize, img_ds.RasterXSize, img_ds.RasterCount),
               gdal_array.GDALTypeCodeToNumericTypeCode(img_ds.GetRasterBand(1).DataType))


#Luego recorro el número de bandas en la imagen (img.shape [2]), 
#insertando los valores en la matriz numpy
for b in range(img.shape[2]):
    img[:, :, b] = img_ds.GetRasterBand(b + 1).ReadAsArray()
    
#tengo q reshape la imagen. 
new_shape = (img.shape[0] * img.shape[1], img.shape[2])    

#colocar número de bandas de la imagen
X = img[:, :, :10].reshape(new_shape)

#escribir el número de clusters qu tendrá la clasificación.
k_means = cluster.KMeans(n_clusters=50)
k_means.fit(X)

X_cluster = k_means.labels_
X_cluster = X_cluster.reshape(img[:, :, 0].shape)

plt.figure(figsize=(20,20))
plt.imshow(X_cluster, cmap="hsv")

plt.show()    

#guardar la clasificación
ds = gdal.Open("sentinel2/s2_20171215_stackreflec.tif")
band = ds.GetRasterBand(2)
arr = band.ReadAsArray()
[cols, rows] = arr.shape
format = "GTiff"
driver = gdal.GetDriverByName(format)
outDataRaster = driver.Create("sentinel2/s2_20171215_clasnosup.tif", rows, cols, 1, gdal.GDT_Byte)
outDataRaster.SetGeoTransform(ds.GetGeoTransform())##sets same geotransform as input
outDataRaster.SetProjection(ds.GetProjection())##sets same projection as input
outDataRaster.GetRasterBand(1).WriteArray(X_cluster)
outDataRaster.FlushCache() ## remove from memory
del outDataRaster ## delete the data (not the actual geotiff)   
outDataRaster.FlushCache() ## remove from memory
del outDataRaster ## delete the data (not the actual geotiff)