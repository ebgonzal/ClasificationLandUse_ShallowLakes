# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 22:29:29 2021

@author: Belen
"""

############################################################################
#Calcular la matriz de distancia euclidiana para las clasificaciones de la lagunas

#paquetes
import numpy as np
import rasterio
from scipy.spatial.distance import cdist

image_path = ("C:/Users/..._clasnosup.tif"

#Abrir el raster
with rasterio.open(image_path) as src:
    # Read the raster band as a numpy array
    classified_image = src.read(1)

rows, cols = classified_image.shape
pixel_matrix = classified_image.reshape(rows * cols)

# Calcular la distancia eucludiana
distance_matrix = cdist(pixel_matrix, pixel_matrix, metric='euclidean')

print(distance_matrix)


#############################################################################
#Selección de agrupamiento y corte para la dendogramas con la distancia euclidiana
#calculada previamente
#############################################################################

# 1.Agrupamientos
df= distance_matrix

#Cluster jerarquico con diferentes métodos
clust_single = linkage(df, method='single')  # Single Linkage
clust_average = linkage(df, method='average')  # UPGMA
clust_ward = linkage(df, method='ward')  # Ward
clust_complete = linkage(df, method='complete')  # Complete Linkage
clust_centroid = linkage(df, method='centroid')  # Centroid

# Plot dendrogramas
plt.figure()
dendrogram(clust_single)
plt.title('Single Linkage')
plt.figure()
dendrogram(clust_average)
plt.title('Average Linkage')
plt.figure()
dendrogram(clust_ward)
plt.title('Ward Linkage')
plt.figure()
dendrogram(clust_complete)
plt.title('Complete Linkage')
plt.figure()
dendrogram(clust_centroid)
plt.title('Centroid Linkage')

# Calculatar correlacion cophenetica para cada método
coph_single, coph_average, coph_ward, coph_complete, coph_centroid = \
    cophenet(clust_single, PFTgower), cophenet(clust_average, PFTgower), \
    cophenet(clust_ward, PFTgower), cophenet(clust_complete, PFTgower), \
    cophenet(clust_centroid, PFTgower)

print('Cophenetic correlation - Single Linkage:', coph_single)
print('Cophenetic correlation - Average Linkage:', coph_average)
print('Cophenetic correlation - Ward Linkage:', coph_ward)
print('Cophenetic correlation - Complete Linkage:', coph_complete)
print('Cophenetic correlation - Centroid Linkage:', coph_centroid)

# setear el mejor método
classification = clust_average

###########################################################################
# 2.Criterios de corte
#Cuando se elige mejor dendograma hay que definir corte para ver cuantos grupos hay

#Máximo salto
print(classification[:, 2])  

# Similitud 50%
sim_max = np.max(classification[:, 2])
sim_min = np.min(classification[:, 2])
sim_50 = (sim_max - sim_min) / 2
print('Similarity 50%:', sim_50)

# Números pre-definidos de grupos
groups = []
for k in range(1, 6):
    group = pd.Series(pd.cut(classification[:, 2], bins=k, labels=False))
    groups.append(group)
print('Predefined number of groups (1-5):', groups)

# Similarity cutoff
similarity_cutoff = sim_50
group_sim50 = pd.Series(pd.cut(classification[:, 2], bins=[0, similarity_cutoff, np.max(classification[:, 2])],
                               labels=False))
print('Groups with similarity cutoff (50%):', group_sim50)

# Guardar los grupos
group_sim50_df = pd.DataFrame(group_sim50, columns=['Groups'])
group_sim50_df.to_csv('groups_sim50.csv', index=False)




