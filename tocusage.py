#!/usr/bin/env python3

#Test for the computation of the
#TOC= Total Operating Charcateristic Curve
#Author:S. Ivvan Valdez 
#Centro de Investigación en Ciencias de Información Geoespacial AC
#Querétaro, México.


# if __name__ == '__main__':
import tocpf as toc
import pandas as pd
import numpy as np
import importlib
import matplotlib.pyplot as plt
from scipy.stats import lognorm
import statsmodels.api as sm
from scipy.stats import shapiro
from scipy.stats import normaltest
import os
import time
#Loading training data,  
dataY=pd.read_csv('../data/Morelia_train_Y.csv')
dataX=pd.read_csv('../data/Morelia_train_X.csv')
lat=dataX.lon.to_numpy()
lon=dataX.lat.to_numpy()
label=dataY.incremento_urbano.to_numpy()


#Selecting a feature and class labels
#feature=dataX.dist_urbano.to_numpy()
#feature=dataX.pendiente.to_numpy()
#feature=dataX.dist_anps.to_numpy()
#feature=dataX.dist_agua.to_numpy()
#feature=dataX.dist_vegetacion.to_numpy()
#feature=dataX.dist_centro.to_numpy()
#feature=dataX.dist_carreteras.to_numpy()
feature=dataX.costo.to_numpy()

####################################################################
##--Fisrt part, TOC and probability density function computation--##
importlib.reload(toc)
tstart = time.time()
T=toc.TOCPF(rank=feature,groundtruth=label)
tend = time.time()
print("Elapsed time for computing the TOC, find an adequate discretization, computing CDF,PF, DPF and their smooth versions:",tend-tstart, "seconds")

T.featureName='Costo'
T.plot() #TOC using the original data
T.plot(kind='discretization') #TOC using the discrete approximation
T.plot(kind='CDF') #Cummulative distribution function Hits vs Ranks
T.plot(kind='CDF',options=['vlines'])
T.plot(kind='PF',options=['vlines']) #Probability function (mass or density from discrete or continuous ranks respectively)
T.plot(kind='DPF') #Derivative or difference of the probability function (first difference or derivative from discrete or continuous ranks respectively)
T.plot(kind='smoothPF') #Smoothed Probability function
T.plot(kind='smoothDPF') #Smoothed Probability function
T.plot(kind='smoothPF',options=['quartiles']) #Smoothed Probability function
T.plot(kind='smoothPF',options=['quartiles','vlines']) #Smoothed Probability function
T.plot(kind='smoothDPF',options=['quartiles']) #Smoothed Probability function


#Assingning probabilities to a set of ranks in a raster
tstart = time.time()
prob=T.rank2prob(feature)
tend = time.time()
print("Elapsed time for computing the probability of ",len(prob),"rank values", tend-tstart, "seconds")
T.rasterize(prob,lat,lon)
T.plot(kind='raster',TOCname='Probability of presence according to Cost')
#Simulating precense according to the PDF
tstart = time.time()
sim=T.simulate(feature,T.np)
tend = time.time()
print("Elapsed time for simulating ",T.np,"land changes", tend-tstart, "seconds")

T.rasterize(sim,lat,lon)
T.plot(kind='raster')

#Optional, executing 30 simulations of land-change, and summing all of them
#for i in range(30):
    #sim=sim+T.simulate(feature,T.np)

#T.rasterize(sim,lat,lon)
#T.plot(kind='raster')

#boostrap confidence interval for the area ratio by default only 100 bootstrap samples are used below there is an example using 1000
tstart = time.time()
T.plot(kind='histogram')
tend = time.time()
print("Elapsed time for bootstraping 100 samples", tend-tstart, "seconds")


T.plot(options=['boostrapCI'])
T.plot(kind='discretization',options=['boostrapCI'])
T.plot(kind='CDF',options=['boostrapCI']) #Cummulative distribution function Hits vs Ranks
T.plot(kind='PF',options=['boostrapCI']) #Probability function (mass or density from discrete or continuous ranks respectively)
T.plot(kind='DPF',options=['boostrapCI']) #Derivative or difference of the probability function (first difference or derivative from discrete or continuous ranks respectively)
T.plot(kind='smoothPF',options=['boostrapCI']) #Smoothed Probability function
T.plot(kind='smoothDPF',options=['boostrapCI']) #Smoothed Probability function
T.plot(kind='smoothPF',options=['quartiles','boostrapCI']) #Smoothed Probability function
T.plot(kind='smoothDPF',options=['quartiles','boostrapCI']) #Smoothed Probability function


#Computing a boostrap confidence interval for the area
T.boostrapCI(nboostrap=1000,CImin=0.02,CImax=0.98)
T.plot(kind='histogram')











T.kind #Discrete or continuous
T.ndiscretization #Data size in the discrete approximation
T.ndata #Data size of the orginal data set and the TOC

T.HpFA  #Hits + False Alarms of the original TOC of size ndata
T.Hits  #Array of Hits of the original TOC
T.rank[T.isorted] #Sorted ranks, rank is the original array, isorted stores the indices to sort the rank
T.Thresholds #These are the Thresholds to build the original TOC, they are actually equal to rank[isorted] as above.
T.rank[T.iunique] #Unique rank values, the array iunique es True in the last non-repeated rank
T.Hits[T.iunique] #Hits actually these are the hits that are part of the TOC function
T.HpFA[T.iunique] #Hits + false alarms, the unique array shows the actual TOCs values, it is useful when some ranks values are repeated, hence some thresholds could present "jumps" in the X and Y coordinates of the TOC.





T.ndiscretization
T.dHits
T.drank
T.dHpFA
T.dThresholds
T.icontinuous

T.CDF
T.PF
T.smoothPF



#All the variables of lengths or counts start with a n
T.ndata #Number of data, this is the size of rank, Threshold, Hits, HpFA.
T.np # Number of data with label=1 (presence)
T.ndiscretization #Number of discrete equally spaced points in the rank domain to approximate the TOC, in such domain and computing the PDF

#All the array of indices start with an i
T.isorted #Indices to sorting the rank
T.iunique #Logical it is 1 at the last of the unique values in the Threshold array, that is T.Thresholds[T.iunique] return unique rank values
T.icontinuous #Indicates whether a point in the discretization has a neighbor, so it is continuous to one or both sides.


#Other useful variables
T.kind #It is continuous, semicontinuous opr discrete
T.area #Area under the curve minus the last triangle of the parallelogram. To be comparable with the parallelogram
T.areRatio #area/ area of the parallelogram


