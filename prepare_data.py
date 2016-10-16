"""

split data into training data and testing data in two separated files
"""
import numpy as np
import re


"""
Split Ryan's data into two parts: TRAIN and TEST with k_fold cross validation
"""
def split_data_ryan(INPUT,TRAIN,TEST,k_fold = 5):
    # k-fold cross-validation
    OUTPUT = './data/Ryan/10KLabeledTweets_formatted.txt'
    # properly format the data
    output = open(OUTPUT, 'w')
    output.write('Tweet ID\tInformation Source\tInformation Type\tDisaster-related\tTweet Text')
    tweets_count = 0
    with open(INPUT) as f:
        for line in f.readlines():
            # check if this line as a proper formatted tweet
            if len(line.split('\t')) == 5:
                output.write('\n')
                output.write(line.strip())
                tweets_count = tweets_count + 1
            else:
                output.write(' ' + line.strip().replace('\t', ' '))

    # data = np.loadtxt(OUTPUT, dtype='str', delimiter='\t', skiprows=1)
    # print data.shape

    #
    # # for i in range(20):
    # #     print data[i]
    # np.savetxt(TEST, data[:test_set_count], fmt='%s', delimiter='\t')
    # np.savetxt(TRAIN, data[test_set_count:], fmt='%s', delimiter='\t')

    test_set_count = tweets_count/k_fold
    test_output = open(TEST, 'w')
    train_output = open(TRAIN, 'w')
    with open(OUTPUT) as f:
        data = f.readlines()
        for line in data[1:test_set_count]:
            test_output.write(line)
        for line in data[test_set_count:]:
            train_output.write(line)

"""
Split CrisisLex's data into two parts: TRAIN and TEST with k_fold cross validation
"""
def split_data_cl(INPUT,TRAIN,TEST,k_fold = 5):
    # properly format the data
    test_output = open(TEST, 'w')
    train_output = open(TRAIN, 'w')
    with open(INPUT) as f:
        data = f.readlines()
        test_set_count = len(data) / k_fold
        for line in data[1:test_set_count]:
            test_output.write(line)
        for line in data[test_set_count:]:
            train_output.write(line)

"""
split both training and testing data into various files, one for each label
"""
def split_data_cl_label(FILE, prefix, labels):
    data = {}
    data_size = {}
    with open(FILE) as f:
        for line in f.readlines():
            label = line.split('\t')[3]
            tweet = line.split('\t')[4]
            if label in labels.keys():
                if label not in data:
                    data[label] = tweet
                    data_size[label] = 1
                else:   # append
                    data[label] = data[label] + tweet
                    data_size[label] = data_size[label] + 1
            else:
                print "label does not exist", label
    print data_size
    for file, content in data.items():
        f = open('./data/CrisisLex/' + prefix + '_' + labels[file] + '.txt', 'w')
        f.write(content)
        f.close()


labels = {'Not related' : 'not_related', 'Related and informative' : 'informative', 'Related - but not informative' : 'not_informative', 'Not applicable' : 'not_applicable'}
split_data_cl_label('./data/training_tweets.txt', 'train', labels)
split_data_cl_label('./data/testing_tweets.txt', 'test', labels)
