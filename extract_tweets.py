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
                    a = a.split(',')
                    tweet = ','.join([a[i] for i in xrange(0, len(a) - columns + 1)])
                    b.append(tweet)
                    b += [a[i] for i in xrange(len(a) - columns + 1, len(a))]
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
tweet_only, with_sentiment, with_informative, without_tweet = False, False, False, True
disaster_array = ["napa_earthquake", "michigan_storm", "california_fire", "washington_mudslide", "iowa_stf", "iowa_storm", "jersey_storm",
                  "oklahoma_storm", "iowa_stf_2", "vermont_storm", "virginia_storm", "texas_storm", "washington_storm",
                  "washington_wildfire", "newyork_storm"]

area = ["affected_filtered", "unaffected_filtered"]
type = ["hash", "classify"]

# extract tweet_only
if tweet_only:
    for ij in disaster_array:
        for i in area:
            for j in type:
                for file in glob.glob(Params.gesis_disaster_folder + ij + "/" + ij + "_" + i + "_" + j + ".txt"):
        #for file in glob.glob(Params.gesis_disaster_folder + "/" + ij + "/" + ij .txt"):
                    basepath, filename = os.path.split(file)
                    file_out = Params.tweet_folder + filename
                    extract_tweets(file, file_out, type='tweet_only')

# add sentiment to data
if with_sentiment:
    for ij in disaster_array:
        for i in area:
            for j in type:
                for file in glob.glob(Params.gesis_disaster_folder + ij + "/" + ij + "_" + i + "_" + j + ".txt"):
    #for file in glob.glob(Params.gesis_disaster_folder + "/*/*.txt"):
                    basepath, filename = os.path.split(file)
                    file_out = Params.with_sentiment_folder + filename
                    #print file_out
                    extract_tweets(file, file_out, type='with_sentiment')

# add informative to tweets
if with_informative:
    for file in glob.glob(Params.with_sentiment_folder + "*.txt"):
        basepath, filename = os.path.split(file)
        file_out = Params.with_informative_folder + filename
        extract_tweets(file, file_out, type='with_informative')

# extract statistics without tweet
if without_tweet:
    for ij in disaster_array:
        for i in area:
            for j in type:
                #print str(Params.with_sentiment_folder + ij + "_" + i + "_" + j + ".txt")
                for file in glob.glob(Params.with_sentiment_folder + ij + "_" + i + "_" + j + ".txt"):
    #for file in glob.glob(Params.with_sentiment_folder + "*.txt"):
                    basepath, filename = os.path.split(file)
                    #print filename
                    file_out = Params.without_tweet_folder + filename
                    #print file_out
                    extract_tweets(file, file_out, type='without_tweet')

