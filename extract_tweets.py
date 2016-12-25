import numpy as np
import re
import os.path
import csv
import glob
import datetime
import calendar
from Utils import distance
from Params import Params
csv.field_size_limit(1000000)


"""
multiple purpose function, e.g., extract tweet only, add sentiment, extract statistics without tweet
"""
def extract_tweets(tweet_input, tweet_output, delimiter=",", tweet_index=0, type='tweet_only'):
    print 'extracting...', tweet_input
    if type == 'tweet_only':
        columns = 5
    elif type == 'with_sentiment':
        basepath, filename = os.path.split(file)
        label_file = Params.label_folder + filename
        if not os.path.isfile(label_file):
            return
        labels = np.loadtxt(label_file)
        j = 0
        columns = 5
    elif type == 'without_tweet':
        columns = 6
    with open(tweet_input, 'rU') as f:
        with open(tweet_output, "w") as f2:
            for b in f:
                arr = []

                if len(b.split(',')) >= columns:
                    st = ""
                    b = b.split(',')
                    for i in xrange(0, len(b) - columns + 1):
                        if i == len(b) - columns:
                            st += b[i]
                        else:
                            st += b[i] + ","
                    arr.append(st)
                    for i in xrange(len(b) - columns + 1, len(b)):
                        arr.append(b[i])
                    b = arr
                elif len(b) < columns:
                    print len(b), b

                if type == 'tweet_only':
                    s = re.sub('[\s]+|&amp;', ' ', b[tweet_index])  # Remove additional white spaces
                    s = re.sub(r'https?:\/\/.*\/[a-zA-Z0-9]*', '', s)  # Remove hyperlinks
                    f2.write(s + "\n")
                elif type == 'with_sentiment':
                    line = str(b[0]) + ',' + str(b[1]) + ',' + str(int(b[2])) + ',' + str(float(b[3])) + ',' + str(float(b[4].strip('\n'))) + ',' + str(int(labels[j])) + '\n'
                    f2.write(line)
                    j = j + 1
                elif type == 'without_tweet':
                    t = calendar.timegm(datetime.datetime.strptime(b[1].strip(), "%Y-%m-%d %H:%M:%S").timetuple())
                    d = distance(float(b[3]), float(b[4]), 38.2414392,-122.3128157)
                    f2.write(str(b[1])+ '\t' + str(t) + '\t' + str(int(b[2]))  + '\t' + str(float(b[3])) + '\t' + str(float(b[4])) + '\t' + str(int(b[5])) + '\t' + str(d) + '\n')

# extract tweet_only
tweet_only, with_sentiment, without_tweet = False, True, False

if tweet_only:
    for file in glob.glob(Params.gesis_disaster_folder + "*/*.txt"):
        basepath, filename = os.path.split(file)
        file_out = Params.tweet_folder + filename
        extract_tweets(file, file_out, type='tweet_only')

# add sentiment to data
if with_sentiment:
    for file in glob.glob(Params.gesis_disaster_folder + "/*/*.txt"):
        basepath, filename = os.path.split(file)
        file_out = Params.with_sentiment_folder + filename
        extract_tweets(file, file_out, type='with_sentiment')

# extract statistics without tweet
if without_tweet:
    for file in glob.glob(Params.with_sentiment_folder + "*.txt"):
        basepath, filename = os.path.split(file)
        file_out = Params.without_tweet_folder + filename
        extract_tweets(file, file_out, type='without_tweet')