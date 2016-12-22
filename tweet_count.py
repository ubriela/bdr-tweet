import re
import glob
import csv


TWEET_PATH = "./data/michigian_flood/affected_output_tweet/"
count = 0
for file in glob.glob(TWEET_PATH + '*/*.txt'):
    filename = re.findall('[^\\\\/]+', file)[-1]
    with open(file, 'rU') as f:
        rd = csv.reader(f, delimiter=",")
        for i in rd:
            count += 1

print count
