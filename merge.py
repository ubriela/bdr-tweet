import numpy as np
import glob
import re
import os
# DATA_PATH = 'data/gesis/2014-08/state_filter/state_2014-08-31/'
DATA_PATH = 'data/Michigan/unaffected_hash_filtered/'
state_stats = {}

for file in glob.glob(DATA_PATH + '*.txt'):
    filename = re.findall('[^\\\\/]+', file)[-1]
    dir_path = os.path.dirname(file)
    print dir_path, filename, filename.split('_')[0]
    with open(dir_path + '/' + filename.split('_')[1] + '.txt', 'a') as outfile:
        with open(file) as infile:
            outfile.write(infile.read())

