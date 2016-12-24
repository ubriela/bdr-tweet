import numpy as np
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
    if type == 'tweet_only':
        columns = 5
    elif type == 'with_sentiment':
        basepath, filename = os.path.split(file)
        labels = np.loadtxt(Params.label_folder + filename)
        j = 0
        columns = 5
    elif type == 'without_tweet':
        columns = 6
    with open(tweet_input, 'rU') as f:
        with open(tweet_output, "w") as f2:
            rd = csv.reader(f, delimiter=delimiter, quotechar='|')
            for a in rd:
                arr = []

                if len(a) > columns:
                    st = ""
                    for i in xrange(0, len(a) - columns + 1):
                        if i == len(a) - columns:
                            st += a[i]
                        else:
                            st += a[i] + ","
                    arr.append(st)
                    for i in xrange(len(a) - columns + 1, len(a)):
                        arr.append(a[i])
                    a = arr
                elif len(a) < columns:
                    print len(a)

                if type == 'tweet_only':
                    f2.write(a[tweet_index] + "\n")
                elif type == 'with_sentiment':
                    line = str(a[0]) + ',' + str(a[1]) + ',' + str(int(a[2])) + ',' + str(float(a[3])) + ',' + str(float(a[4])) + ',' + str(int(labels[j])) + '\n'
                    f2.write(line)
                    j = j + 1
                elif type == 'without_tweet':
                    t = calendar.timegm(datetime.datetime.strptime(a[1].strip(), "%Y-%m-%d %H:%M:%S").timetuple())
                    d = distance(float(a[3]), float(a[4]), 38.2414392,-122.3128157)
                    f2.write(str(a[1])+ '\t' + str(t) + '\t' + str(int(a[2]))  + '\t' + str(float(a[3])) + '\t' + str(float(a[4])) + '\t' + str(int(a[5])) + '\t' + str(d) + '\n')

# extract tweet_only
tweet_only, with_sentiment, without_tweet = False, True, True

if tweet_only:
    for file in glob.glob(Params.gesis_disaster_folder + "*.txt"):
        basepath, filename = os.path.split(file)
        file_out = Params.tweet_folder + filename
        extract_tweets(file, file_out, type='tweet_only')

# add sentiment to data
for file in glob.glob(Params.gesis_disaster_folder + "*.txt"):
    basepath, filename = os.path.split(file)
    file_out = Params.gesis_disaster_folder + 'with_sentiment/' + filename
    extract_tweets(file, file_out, type='with_sentiment')

# extract statistics without tweet
for file in glob.glob(Params.gesis_disaster_folder + 'with_sentiment/' + "*.txt"):
    basepath, filename = os.path.split(file)
    file_out = Params.gesis_disaster_folder + 'without_tweet/' + filename
    extract_tweets(file, file_out, type='without_tweet')