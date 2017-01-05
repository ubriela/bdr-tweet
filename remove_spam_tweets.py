"""
remove spam tweets from users that has more than K number of tweets
"""

import numpy as np
import collections
from sets import Set
from Params import Params
from datetime import datetime


disaster_array = ["napa_earthquake", "michigan_storm", "california_fire", "washington_mudslide", "iowa_stf", "iowa_storm", "jersey_storm",
                  "oklahoma_storm", "iowa_stf_2", "vermont_storm", "virginia_storm", "texas_storm", "washington_storm",
                  "washington_wildfire", "newyork_storm"]

K = 15   # tweets created by users with more than K tweets are considered spams
d_duration = Params.disaster_duration

"""
remove tweets from spam users, who created more than K tweets
"""
def remove_spam_tweets(input_file, non_spam_tweets, spam_tweets, delimeter=',', user_id_index=0):
    global K
    print K
    user_ids = []
    data = []
    with open(input_file, 'rU') as fg:
        for g in fg:
            a = (g.split(','))
            try:
                user_ids.append(a[-3])
                data.append(a)
            except IndexError:
                continue

    data = np.array(data)

    #print user_ids
    #user_ids = np.loadtxt(input_file, dtype= 'int64', delimiter=delimeter, usecols = ([len()]))
    map_index = {}
    for i in range(len(user_ids)):
        map_index[user_ids[i]] = i
    counter = dict(collections.Counter(user_ids))

    non_spam_user_ids = Set([k for k in counter.keys() if counter[k] <= K])

    valid_rows = np.array([id in non_spam_user_ids for id in user_ids])
    invalid_rows = np.array([id not in non_spam_user_ids for id in user_ids])

    #data = np.loadtxt(input_file, dtype= 'str', delimiter=delimeter)
    non_spam_data = data[valid_rows]
    spam_data = data[invalid_rows]

    print 'Number of spam tweets: ', len(spam_data), '(', int((len(spam_data)+ 0.0)/len(user_ids) * 100), '%)'
    np.savetxt(non_spam_tweets, non_spam_data, fmt='%s', delimiter=delimeter)
    np.savetxt(spam_tweets, spam_data, fmt='%s', delimiter=delimeter)

for ij in disaster_array:
    print d_duration[ij]
    K = 15
    date_format = "%m-%d-%Y %H:%M:%S"
    a = datetime.strptime(d_duration[ij][0], date_format)
    b = datetime.strptime(d_duration[ij][1], date_format)
    delta = b - a
    #print delta.days
    K = K * (delta.days + 1)
    f = ["./data/disasters/" + ij + "/" + ij + "_affected_unfiltered.txt",
         "./data/disasters/" + ij + "/" + ij + "_unaffected_unfiltered.txt"]
    for i in f:
        NON_SPAM_FILE = i[:-4] + "_non_spam.txt"
        SPAM_FILE = i[:-4] + "_spam.txt"
        remove_spam_tweets(i, NON_SPAM_FILE, SPAM_FILE)