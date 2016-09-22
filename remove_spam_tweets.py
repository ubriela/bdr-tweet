"""
remove spam tweets from users that has more than K number of tweets
"""

import numpy as np
import collections
from sets import Set

INPUT_FILE = "./data/output/20160903.txt"
OUTPUT_FILE = "./data/output/cleaned_tweets.txt"

K = 3   # tweets created by users with more than K tweets are considered spams

"""
remove tweets from spam users, who created more than K tweets
"""
def remove_spam_tweets(input_file, output_file, delimeter='\t', user_id_index=1):
    global K
    user_ids = np.loadtxt(input_file, dtype= 'int64', delimiter=delimeter, usecols = ([1]))
    map_index = {}
    for i in range(len(user_ids)):
        map_index[user_ids[i]] = i
    counter = dict(collections.Counter(user_ids))
    non_spam_user_ids = Set([k for k in counter.keys() if counter[k] <= K])
    valid_rows = np.array([id in non_spam_user_ids for id in user_ids])

    data = np.loadtxt(input_file, dtype= 'str', delimiter=delimeter)
    data = data[valid_rows]

    print 'Number of spam tweets removed: ', len(user_ids) - len(data), '(', int((len(user_ids) - len(data) + 0.0)/len(user_ids) * 100), '%)'
    np.savetxt(output_file, data, fmt='%s', delimiter=delimeter)

remove_spam_tweets(INPUT_FILE, OUTPUT_FILE)