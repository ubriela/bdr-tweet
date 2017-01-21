"""
remove spam tweets from users that has more than K number of tweets
"""

import numpy as np
import collections
from sets import Set
from Params import Params
from datetime import datetime
import operator



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

    #data = np.array(data)

    #print user_ids
    #user_ids = np.loadtxt(input_file, dtype= 'int64', delimiter=delimeter, usecols = ([len()]))
    map_index = {}
    for i in range(len(user_ids)):
        map_index[user_ids[i]] = i
    counter = dict(collections.Counter(user_ids))
    #sorted_x = sorted(counter.items(), key=operator.itemgetter(1))
    #print sorted_x[len(sorted_x) - 50 :-1]

    non_spam_user_ids = Set([k for k in counter.keys() if counter[k] <= K])

    valid_rows = []

    for id in data:
        if id[-3] in non_spam_user_ids:
            valid_rows.append(1)
        else:
            valid_rows.append(0)


    non_spam_data = 0
    spam_data = 0
    #print valid_rows
    with open(non_spam_tweets,"wb") as f2:
        for i in xrange(len(valid_rows)):
            if int(valid_rows[i]) == 1:
                f2.write(",".join(data[i]))
                non_spam_data += 1

    with open(spam_tweets, "wb") as f3:
        for i in xrange(len(valid_rows)):
            if int(valid_rows[i]) == 0:
                f3.write(",".join(data[i]))
                spam_data += 1


    print 'Number of spam tweets: ', (spam_data), '(', int(((spam_data)+ 0.0)/len(user_ids) * 100), '%)'
    print "Number of Non Spam users: ", len(non_spam_user_ids)
    print "Number of Spam users: ", len(counter) - len(non_spam_user_ids)
    #print "Number of Non Spam users: ", ((non_spam_user * 1.0) / (spam_user + non_spam_user)) * 100
    #print "Number of Spam users : ", ((spam_user * 1.0) / (spam_user + non_spam_user)) * 100
    #np.savetxt(non_spam_tweets, non_spam_data, fmt='%s', delimiter=delimeter)
    #np.savetxt(spam_tweets, spam_data, fmt='%s', delimiter=delimeter)

for ij in disaster_array:

    #print d_duration[ij]
    print ij
    #if ij != "newyork_storm":
    #    continue
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