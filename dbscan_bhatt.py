# -*- coding: utf-8 -*-
"""
DBSCAN: Density-Based Spatial Clustering of Applications with Noise 
        use Bhattacharyya Distance.
"""

# Author: Jim Huang <huangjiancong863@gmail.com>
#         
#
# License: MIT License

import math
import numpy as np
import random

UNCLASSIFIED = False
NOISE = None

def bhat_distance(a, b):
    """Caculate the Bhattacharyya Distance"""
    if not len(a) == len(b):
        raise ValueError("a and b must be of the same size")
    return math.log(sum((math.sqrt(u * w) for u, w in zip(a, b))))

def eucli_distance(a, b):
    """Caculate the Euclidean Distance"""
    if not len(a) == len(b):
        raise ValueError("a and b must be of the same size")
    return math.sqrt(np.power(a-b, 2).sum())

def eps_neighborhood(a, b, eps):
	return bhat_distance(a, b) < eps
    # return eucli_distance(a, b) < eps


def region_query(m, point_id, eps):
    n_points = m.shape[0]
    seeds = []
    for i in range(0, n_points):
        if eps_neighborhood(m[point_id,:], m[i,:], eps):
            seeds.append(i)
    return seeds

def expand_cluster(m, classifications, point_id, cluster_id, eps, minpts):
    seeds = region_query(m, point_id, eps)
    if len(seeds) < minpts:
        classifications[point_id] = NOISE
        return False
    else:
        classifications[point_id] = cluster_id
        for seed_id in seeds:
            classifications[seed_id] = cluster_id
            
        while len(seeds) > 0:
            current_point = seeds[0]
            results = region_query(m, current_point, eps)
            if len(results) >= minpts:
                for i in range(0, len(results)):
                    result_point = results[i]
                    if classifications[result_point] == UNCLASSIFIED or \
                       classifications[result_point] == NOISE:
                        if classifications[result_point] == UNCLASSIFIED:
                            seeds.append(result_point)
                        classifications[result_point] = cluster_id
            seeds = seeds[1:]
        return True

def DBSCAN(m, eps, minpts):
    """Density-Based Spatial Clustering of Applications with Noise algo 
       Caculate to Bhattacharyya Distance
    Parameters
	----------
	eps : float
		The maximum distance between two samples for them to be considered as in
		the same neighborhood.
	minpts : int
		The number of samples (or total weight) in a neighborhood for a point to
		be considered as
		a core point. This includes the point itself.
	dataset : array_like
		The clustering sample states.

	Return
	------
	classification : array_like
		The clustered group of each data.

    Example
    -------
    >>> from dbscan_bhatt import DBSCAN
    >>> import numpy as np
    >>> X = np.arraynp.array([[1, 2, 1], [2, 2, 2], [2, 3, 3], 
    ...               [8, 7, 7], [8, 8, 8], [25, 80, 50]])
    >>> clustering = clustering = DBSCAN(X3, 3, 2)
    >>> clustering.labels_
    array([ 0,  0,  0,  1,  1, None])
	"""
    cluster_id = 1
    n_points = m.shape[0]
    classifications = [UNCLASSIFIED] * n_points
    for point_id in range(0, n_points):
        # point = m[:,point_id]
        if classifications[point_id] == UNCLASSIFIED:
            if expand_cluster(m, classifications, point_id, cluster_id, eps, minpts):
                cluster_id = cluster_id + 1
    return classifications