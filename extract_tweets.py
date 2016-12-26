import numpy as np
import re
import os.path
import csv
import glob
import datetime
import calendar
from Utils import distance
from Params import Params


"""
multiple purpose function, e.g., extract tweet only, add sentiment, extract statistics without tweet
"""
def extract_tweets(tweet_input, tweet_output, tweet_index=0, type='tweet_only'):
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
    elif type == 'with_informative':
        columns = 6
    elif type == 'without_tweet':
        columns = 6

    with open(tweet_input, 'rU') as f:
        with open(tweet_output, "w") as f2:
            for a in f:
                b = []
                if len(a.split(',')) >= columns:
                    tweet = ""
                    a = a.split(',')
                    for i in xrange(0, len(a) - columns + 1):
                        if i == len(a) - columns:
                            tweet += a[i]
                        else:
                            tweet += a[i] + ","
                    b.append(tweet)
                    for i in xrange(len(a) - columns + 1, len(a)):
                        b.append(a[i])
                elif len(b) < columns:
                    print len(b), b
                    j = j + 1
                    continue

                if type == 'tweet_only':
                    s = re.sub('[\s]+|&amp;', ' ', b[tweet_index])  # Remove additional white spaces
                    s = re.sub(r'https?:\/\/.*\/[a-zA-Z0-9]*', '', s)  # Remove hyperlinks
                    f2.write(s + "\n")
                elif type == 'with_sentiment':
                    line = str(b[0]) + ',' + str(b[1]) + ',' + str(int(b[2])) + ',' + str(float(b[3])) + ',' + str(float(b[4].rstrip('\n'))) + ',' + str(int(labels[j])) + '\n'
                    f2.write(line)
                    j = j + 1
                elif type == 'with_informative':
                    line = str(b[0]) + ',' + str(b[1]) + ',' + str(int(b[2])) + ',' + str(float(b[3])) + ',' + str(
                        float(b[4].rstrip('\n'))) + ',' + str(int(b[5])) + '\n'
                    f2.write(line)
                elif type == 'without_tweet':
                    t = calendar.timegm(datetime.datetime.strptime(b[1].strip(), "%Y-%m-%d %H:%M:%S").timetuple())
                    d = distance(float(b[3]), float(b[4]), 38.2414392,-122.3128157)
                    f2.write(str(b[1])+ '\t' + str(t) + '\t' + str(int(b[2]))  + '\t' + str(float(b[3])) + '\t' + str(float(b[4].rstrip('\n'))) + '\t' + str(int(b[5])) + '\t' + str(d) + '\n')


# setup
tweet_only, with_sentiment, with_informative, without_tweet = False, False, True, False

# extract tweet_only
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

# add informative to tweets
if with_informative:
    for file in glob.glob(Params.with_sentiment_folder + "*.txt"):
        basepath, filename = os.path.split(file)
        file_out = Params.with_informative_folder + filename
        extract_tweets(file, file_out, type='with_informative')

# extract statistics without tweet
if without_tweet:
    for file in glob.glob(Params.with_sentiment_folder + "*.txt"):
        basepath, filename = os.path.split(file)
        file_out = Params.without_tweet_folder + filename
        extract_tweets(file, file_out, type='without_tweet')

