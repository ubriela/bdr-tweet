import urllib
import xml.etree.ElementTree as ET
import numpy as np
import re
from scipy.stats import stats
THRESHOLD_MMI = 0  # This is threshold for earthquake intensity to create the task region.

"""
LON,LAT,PGA,PGV,MMI,PSA03,PSA10,PSA30,STDPGA,URAT,SVEL
LOT 0
LAT 1
MMI 2
"""

debug = True

LAT_SIZE = 201
LON_SIZE = 301
min_lat, min_lon, max_lat, max_lon = 37.382166, -123.561700, 39.048834, -121.061700
lat_spacing = 0.008333 # (max_lat - min_lat)/LAT_SIZE
lon_spacing = 0.008333 # (max_lon - min_lon)/LON_SIZE

urgency_map = np.matrix(np.zeros(shape=(LAT_SIZE, LON_SIZE, 1)))
social_urgency_map = np.matrix(np.zeros(shape=(LAT_SIZE, LON_SIZE, 1)))

file = '/Users/ubriela/git/tweet/data/gesis/state_id_2014-08-24/2014-08-24_06.txt',
file_out = '/Users/ubriela/git/tweet/data/gesis/state_id_2014-08-24/2014-08-24_06_filtered.txt',

"""
filter only tweets in a region, output tweets to another file
"""
def filter_tweets(min_lat, min_lon, max_lat, max_lon):
    data = np.loadtxt(file, dtype= float, delimiter='\t', usecols = (2,3))
    filter_data = np.all([min_lat <= data[:,0], data[:,0] <= max_lat, min_lon <= data[:,1],  data[:,1]<= max_lon], axis=0)


def read_shakemap_xml(url='http://earthquake.usgs.gov/archive/product/shakemap/nc72282711/nc/1431987323474/download/grid.xml'):
    u = urllib.urlopen(url)
    # compute urgency map
    data = u.read()
    root = ET.fromstring(data)
    for child in root.getchildren():
        if debug:
            if child.tag.endswith('event'):
                print child.attrib
            if child.tag.endswith('grid_specification'):
                print child.attrib["lat_min"], child.attrib["lon_min"], child.attrib["lat_max"], child.attrib["lon_max"]
                print child.attrib["nlat"], child.attrib["nlon"], child.attrib["nominal_lat_spacing"], child.attrib["nominal_lon_spacing"]
        if child.tag.endswith('grid_data'):
            grid_data = child.text
            rows = grid_data.strip().split("\n")
            for row in rows:
                values = row.split()
                if float(values[4]) >= THRESHOLD_MMI:
                    lon, lat, mmi = float(values[0]), float(values[1]), float(values[4])
                    # print lat, min_lat, lat_spacing
                    # print round((lat - min_lat + lat_spacing/2) / lat_spacing)
                    lat_index = int((lat - min_lat + lat_spacing/2) / lat_spacing)
                    lon_index = int((lon - min_lon + lon_spacing/2) / lon_spacing)
                    urgency_map[lat_index,lon_index] = mmi

    # compute social urgency map

filter_tweets(min_lat - lat_spacing, min_lon - lon_spacing, max_lat, max_lon)
read_shakemap_xml()

print urgency_map

# stats.entropy([2,3,4], [4,6,8])


"""
given a location, determine its urgency value
"""
def urgency_value(lat, lon):
    lat_index = int(round((lat - min_lat)/lat_spacing))
    lon_index = int(round((lon - min_lon)/lon_spacing))
    return urgency_map[lon_index][lat_index]