import numpy as np
import collections
from sets import Set

INPUT_FILE = "C:/Users/ubriela/Desktop/US_June2016.csv"
OUTPUT_FILE = "C:/Users/ubriela/Desktop/US_June2016_locs.csv"

"""
remove tweets from spam users, who created more than K tweets
"""
def parse_tweets(input_file, output_file, delimeter=','):
    # data = np.loadtxt(input_file, dtype= 'str', delimiter=delimeter, usecols = ([1]))
    # print data.shape
    # np.savetxt(output_file, data, fmt='%s', delimiter=delimeter)
    with open(input_file, "r") as ins:
        array = []
        for line in ins:
            arr = line.split(',')
            if len(arr) == 43:
                print arr

parse_tweets(INPUT_FILE, OUTPUT_FILE)