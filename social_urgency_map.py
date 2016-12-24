import urllib
import xml.etree.ElementTree as ET
import numpy as np
import re
import os
from scipy.stats import stats
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import xml.etree.ElementTree as ET
import csv
import time
import datetime
import calendar
from Utils import distance
csv.field_size_limit(1000000)

from Quad_standard import Quad_standard
from Params import Params

THRESHOLD_MMI = 0  # This is threshold for earthquake intensity to create the task region.
debug = False

LAT_SIZE = 201
LON_SIZE = 301
min_lat, min_lon, max_lat, max_lon = 37.382166, -123.561700, 39.048834, -121.061700                 # shakemap
# min_lat, min_lon, max_lat, max_lon = 32.699134999, -124.358576176, 45.8370813015, -114.720950501    # dyfi map
lat_spacing = 0.008333 # (max_lat - min_lat)/LAT_SIZE
lon_spacing = 0.008333 # (max_lon - min_lon)/LON_SIZE

def cdi_parse_csv(cdi_file='./data/usgs/napa/cdi_zip.xml'):
    tree = ET.parse(cdi_file)
    root = tree.getroot()[0]
    results = []
    for child in root:
        cdi, nresp, dist, lat, lon = str(child[0].text), str(child[1].text), str(child[2].text), str(child[3].text), str(child[4].text)
        if min_lat <= float(lat) <= max_lat and min_lon <= float(lon) <= max_lon:
            results.append((cdi, nresp, dist, lat, lon))
    return results

if False:
    cdi_data = cdi_parse_csv()
    np.savetxt('./data/usgs/napa/cdi_zip.txt', cdi_data, delimiter='\t',  header='cdi\t nresp\t dist\t lat\t lon', fmt='%s')

"""
LON,LAT,PGA,PGV,MMI,PSA03,PSA10,PSA30,STDPGA,URAT,SVEL
LOT 0
LAT 1
MMI 2
"""



urgency_map = np.matrix(np.zeros(shape=(LAT_SIZE, LON_SIZE, 1)))
social_urgency_map_neg = np.matrix(np.zeros(shape=(LAT_SIZE, LON_SIZE, 1)))
social_urgency_map = np.matrix(np.zeros(shape=(LAT_SIZE, LON_SIZE, 1)))

# file = "./data/gesis/state_id_2014-08-24/2014-08-24_06.txt"
# file_out = "./data/earthquake_sentiment/2014-08-24_06.txt"

file = 'data/NewYork/ny_affected_tweet_hash_filter.txt'
file_out = 'data/NewYork/ny_affected_tweet_hash_filter_tweets.txt'

"""
filter only tweets in a region, output tweets to another file
"""
def filter_tweets(min_lat, min_lon, max_lat, max_lon):
    with open(file) as f:
        with open(file_out, "w") as f2:
            for line in f:
                arr = []
                a = [x.strip() for x in line.split(',')]

                if len(a) > 6:
                    st = ""
                    for i in xrange(0, len(a) - 5):
                        if i == len(a) - 6:
                            st += a[i]
                        else:
                            st += a[i] + ", "
                    arr.append(st)
                    for i in xrange(len(a) - 5, len(a)):
                        arr.append(a[i])
                    a = arr
                lat, lon = float(a[len(a) - 3]), float(a[len(a) - 2])
                print lat, lon
                if min_lat <= lat <= max_lat and min_lon <= lon <= max_lon:
                    f2.write(','.join(a) + '\n')
    # filter_data = np.all([min_lat <= data[:,0], data[:,0] <= max_lat, min_lon <= data[:,1],  data[:,1]<= max_lon], axis=0)


# 'http://earthquake.usgs.gov/archive/product/shakemap/nc72282711/nc/1431987323474/download/grid.xml'
def read_shakemap_xml(url='file:///C:/Users/ubriela/git/tweet/data/usgs/napa/grid.xml'):
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

def read_dyfi_map(file='./data/usgs/napa/cdi_zip.txt'):
    # , dtype = {'names': ('cdi', 'nresp', 'dist', 'lat', 'lon'), 'formats': ('i2', 'i4', 'i4', 'f8', 'f8')}
    data = np.loadtxt(file, skiprows=1, delimiter='\t')
    print 'read dyfi map, cell count', data.shape[0]
    print 'bounding box', min(data[:, 3]), max(data[:, 3]), min(data[:, 4]), max(data[:, 4])

    for row in data:
        if float(row[0]) >= THRESHOLD_MMI:
            lat, lon, mmi = float(row[3]), float(row[4]), float(row[0])
            lat_index = int((lat - min_lat + lat_spacing / 2) / lat_spacing)
            lon_index = int((lon - min_lon + lon_spacing / 2) / lon_spacing)
            urgency_map[lat_index, lon_index] = mmi

    return data

# compute social urgency map
def read_social_map(file='./data/earthquake_sentiment/output.csv'):
    tweet_data = []
    with open(file) as f:
        for line in f:
            a = [x.strip() for x in line.split(',')]
            lat, lon, sentiment = float(a[len(a) - 3]), float(a[len(a) - 2]), int(a[len(a) - 1])
            tweet_data.append([lat,lon,sentiment])
            lat_index = int((lat - min_lat + lat_spacing / 2) / lat_spacing)
            lon_index = int((lon - min_lon + lon_spacing / 2) / lon_spacing)
            if sentiment == -1:
                social_urgency_map_neg[lat_index, lon_index] = social_urgency_map_neg[lat_index, lon_index] + 1.0
            social_urgency_map[lat_index, lon_index] = social_urgency_map[lat_index, lon_index] + 1.0
                # print lat, lon
    return np.array(tweet_data)
# filter_tweets(min_lat - lat_spacing, min_lon - lon_spacing, max_lat, max_lon)
# print os.system("python word2vec_tweet_filter.py ./data/Ryan/10KLabeledTweets_confidence.csv 295 ./data/earthquake_sentiment/2014-08-24_06.txt ./data/earthquake_sentiment/logistic_pred_output.txt ./data/earthquake_sentiment/output.txt 0")


RUN_URGENCY_MAP = False
if RUN_URGENCY_MAP:
# read_shakemap_xml()
    dyfi_data = read_dyfi_map()
    tweet_data = read_social_map()

    urgency_map = urgency_map.A1
    social_urgency_map_neg = social_urgency_map_neg.A1
    social_urgency_map = social_urgency_map.A1

    for i in range(len(urgency_map)):
        if (urgency_map[i] != 0 or  social_urgency_map[i] != 0) and social_urgency_map_neg[i] >= 10:
            index_y = i / LON_SIZE
            index_x = i - (i / LON_SIZE) * LON_SIZE
            print urgency_map[i], '\t', social_urgency_map[i], '\t', social_urgency_map_neg[i], '\t', social_urgency_map_neg[i]/social_urgency_map[i], '\t', index_y * lat_spacing + min_lat, '\t', index_x * lon_spacing + min_lon

# normalize maps
# urgency_map = urgency_map / np.linalg.norm(urgency_map)
# social_urgency_map = social_urgency_map/ np.linalg.norm(social_urgency_map)

# compute KL-divergence
# print cosine_similarity(urgency_map, social_urgency_map)
# for i in range(len(urgency_map)):
#     if social_urgency_map_neg[i] != 0:
#         print urgency_map[i], social_urgency_map_neg[i], social_urgency_map[i], social_urgency_map_neg[i]/social_urgency_map[i]

def data_readin(p):
    tweet_locs = tweet_data[:, :]
    tweet_locs = np.transpose(tweet_locs)
    p.NDIM, p.NDATA = 2, tweet_locs.shape[1]
    p.LOW, p.HIGH = np.amin(tweet_locs, axis=0), np.amax(tweet_locs, axis=0)
    p.tweet_data, p.dyfi_data = tweet_data, dyfi_data
    return tweet_locs

# content of tweets
# locations of tweets
# param = Params(1000, 37.382166, -123.561700, 39.048834, -121.061700)
# tweet_locs = data_readin(param)

# tree = Quad_standard(tweet_locs, param)
# tree.buildIndex()