__author__ = 'ubriela'

import numpy as np
import math
from math import atan2, degrees, pi
from Params import Params


def mbr_to_path(box):
    return [(box[0][0], box[0][1]),(box[0][0], box[1][1]),(box[1][0], box[1][1]),(box[1][0], box[0][1]),(box[0][0], box[0][1])]

"""
Return all cell index in the area covered by MBR
"""
def mbr_to_cellids(mbr, param):
    x_width, y_width = param.x_max - param.x_min, param.y_max - param.y_min
    x_min_idx = int(param.GRID_SIZE*(mbr[0][0] - param.x_min)/x_width)
    y_min_idx = int(param.GRID_SIZE*(mbr[0][1] - param.y_min)/y_width)
    x_max_idx = int(param.GRID_SIZE*(mbr[1][0] - param.x_min)/x_width)
    y_max_idx = int(param.GRID_SIZE*(mbr[1][1] - param.y_min)/y_width)

    # print mbr
    # print param.x_min, param.y_min, param.x_max, param.y_max
    # print x_width, y_width, x_min_idx, y_min_idx, x_max_idx, y_max_idx

    # cellids = []
    # for j in range(y_min_idx, y_max_idx + 1):
    #     for i in range(x_min_idx, x_max_idx + 1):
    #         cellids.append(j * param.GRID_SIZE + i)

    return [(j * param.GRID_SIZE + i) for j in range(y_min_idx, y_max_idx + 1) for i in range(x_min_idx, x_max_idx + 1) if param.GRID_SIZE * param.GRID_SIZE>(j * param.GRID_SIZE + i) >= 0]

# Return coordinates of the cell given its index number
def cell_coord(item, param):
    y_idx = item/param.GRID_SIZE
    x_idx = item - y_idx*param.GRID_SIZE
    return param.x_min + x_idx*(param.x_max - param.x_min)/param.GRID_SIZE, param.y_min + y_idx*(param.y_max - param.y_min)/param.GRID_SIZE


def angle_bwn_two_points(lat1,lng1,lat2,lng2):
        dx = lat2 - lat1
        dy = lng2 - lng1
        rads = atan2(-dy,dx)
        # rads %= 2*pi
        rads += pi/2.0;
        return degrees(rads)
    # print angle_bwn_two_points(0,0,1,-1)

def distance_km(lat1, lon1, lat2, lon2):
    """
    Distance between two geographical locations
    """
    R = 6371  # km
    dLat = math.radians(abs(lat2 - lat1))
    dLon = math.radians(abs(lon2 - lon1))
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.sin(dLon / 2) * math.sin(dLon / 2) * math.cos(lat1) * math.cos(
        lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d

if False:
    # test
    box = np.array([[1.5,1.5],[2.5,3.5]])
    param = Params(1000)
    param.GRID_SIZE = 5
    param.x_min,param.y_min,param.x_max,param.y_max = 0,0,5,5
    print mbr_to_cellids(box,param)

