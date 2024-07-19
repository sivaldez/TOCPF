The TOCPF class is intended for computing the Total Operating Characteristic Curve, from a data set and related operations. 

For instance, it intend to detect whether a data set can be considered as cointinuous or discrete in the rank domain (predicting feature values) and Hits counterdomain.
The it computes the TOC and derived Cummulative Distribution Function(CDF), Density or Mass probability function(PF) (depends on the kind of TOC: continuous or discrete),
and first derivative or difference of the PF, depending on the kind of TOC curve, continuous or discrete respectively. 
In addition it has a procedure for smoothing the curves, a rasterization of an array (probabilities or simulations), a simulation procedure for predicting (simulate a random presence according to the PF),
and computation of bootstrap intervals.

For usage example see tocusage.py
