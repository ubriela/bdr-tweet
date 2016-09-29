import numpy as np
import collections
from sets import Set
import re

# INPUT_FILE = "C:/Users/ubriela/Desktop/US_June2016.csv"
INPUT_FILE = "/Users/ubriela/Downloads/US_July2016.csv"
OUTPUT_FILE = "/Users/ubriela/Downloads/US_July2016_filtered.csv"

date_regex = re.compile('[Jun 11]|[Jun 12]|[Jun 13]]')

"""
remove tweets from spam users, who created more than K tweets
"""
def parse_tweets(input_file, output_file, delimeter=','):
    # data = np.loadtxt(input_file, dtype= 'str', delimiter=delimeter, usecols = ([1]))
    # print data.shape
    # np.savetxt(output_file, data, fmt='%s', delimiter=delimeter)
    with open(input_file, "r") as ins:
        # array = []
        for line in ins:
            if date_regex.findall(line):
                print line

parse_tweets(INPUT_FILE, OUTPUT_FILE)