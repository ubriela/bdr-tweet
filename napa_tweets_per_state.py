import numpy as np
import glob
import re

DATA_PATH = 'data/gesis/2014-08/state_filter/'

data = np.loadtxt('data/gesis/state_codes.txt', delimiter='|', skiprows = (1), usecols = (0,1), dtype='str')

state_codes = {}
for row in data:
    state_codes[row[0]] = row[1]

state_stats = {}

for file in glob.glob(DATA_PATH + '/*/*.txt'):
    filename = re.findall('[^\\\\/]+', file)[-1]
    state_code = filename.split('_')[len(filename.split('_')) - 1].split('.')[0]
    tweet_count = sum(1 for line in open(file))
    if state_code in state_stats:
        state_stats[state_code].append(tweet_count)
    else:
        state_stats[state_code] = [tweet_count]

total = 0
for (code, counts) in state_stats.iteritems():
    print state_codes[code], '\t', '\t'.join(map(str, counts))
    total = total + sum(counts)

print total

