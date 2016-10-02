"""
remove spam tweets from users that has more than K number of tweets
"""

import numpy as np
import collections
from sets import Set

INPUT_FILE = "./data/selected_tweets/GMove_LA_tweets_processed.txt"
NON_SPAM_FILE = "./data/selected_tweets/non_spam_GMove_LA_tweets.txt"
SPAM_FILE = "./data/selected_tweets/spam_GMove_LA_tweets.txt"

K = 1000   # tweets created by users with more than K tweets are considered spams

"""
remove tweets from spam users, who created more than K tweets
"""
def remove_spam_tweets(input_file, non_spam_tweets, spam_tweets, delimeter='\t', user_id_index=1):
    global K
    user_ids = np.loadtxt(input_file, dtype= 'int64', delimiter=delimeter, usecols = ([1]))
    map_index = {}
    for i in range(len(user_ids)):
        map_index[user_ids[i]] = i
    counter = dict(collections.Counter(user_ids))

    non_spam_user_ids = Set([k for k in counter.keys() if counter[k] <= K])

    valid_rows = np.array([id in non_spam_user_ids for id in user_ids])
    invalid_rows = np.array([id not in non_spam_user_ids for id in user_ids])

    data = np.loadtxt(input_file, dtype= 'str', delimiter=delimeter)
    non_spam_data = data[valid_rows]
    spam_data = data[invalid_rows]

    print 'Number of spam tweets: ', len(spam_data), '(', int((len(spam_data)+ 0.0)/len(user_ids) * 100), '%)'
    np.savetxt(non_spam_tweets, non_spam_data, fmt='%s', delimiter=delimeter)
    np.savetxt(spam_tweets, spam_data, fmt='%s', delimiter=delimeter)

remove_spam_tweets(INPUT_FILE, NON_SPAM_FILE, SPAM_FILE)