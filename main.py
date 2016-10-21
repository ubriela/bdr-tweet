"""

"""
import os
import platform
from create_vocab_from_tweets import read_data, save_vocab_tweets, make_vocab
from svm_preprocess import get_vocab, read_train_data, read_test_data, save_data
from prepare_data import split_data_ryan, split_data_cl

# using proper library depends on OS type
platform = platform.system()
if platform == 'Windows':
    svm_learn = '.\lib\svm_learn.exe'
    svm_classify = '.\lib\svm_classify.exe'
else:
    svm_learn = './lib/svm_learn'
    svm_classify = './lib/svm_classify'

# PARAMETERS ##############################################
DATASET = "ryan"  # CrisisLex

# merge crisislex datasets into one file ###############################
# os.system("python process_crisislex.py")
# print "Created training data from CrisisLex26"

# prepare training and testing data ###############################

#print os.system("python word2vec.py ./data/CrisisLex/CrisisLex27K.csv 1000")
#print os.system("python word2vec_fast.py ./data/CrisisLex/CrisisLex27K.csv 1000")
print os.system("python word2vec_fast.py ./data/Ryan/10KLabeledTweets_confidence.csv 335")


TRAIN, TEST= "./data/training_tweets.txt", "./data/testing_tweets.txt"
if DATASET == 'cl':
    INPUT = './data/CrisisLex/CrisisLex27K.csv'
    split_data_cl(INPUT, TRAIN, TEST)
    labels_map = {'Not related': -1, 'Related and informative': 1, 'Related - but not informative': 1}
elif DATASET == 'ryan':
    INPUT = './data/Ryan/10KLabeledTweets.txt'
    split_data_ryan(INPUT, TRAIN, TEST)
    labels_map = {'Relevant': 1, 'Not Relevant': -1}

print "Prepared training and testing data"

# create vocabulary ###############################
output_filename = "./data/refined_training_tweets.txt"
vocab_filename = "./data/Tweets.vocab"

refined_tweets, save_tweets = read_data(TRAIN, tweet_index=4)
save_vocab_tweets(save_tweets, output_filename)
make_vocab(refined_tweets, vocab_filename)
print "Created refined training data and vocabulary file"

# prepare training and testing inputs ###############################
test_text_index, test_label_index, train_text_index, train_label_index = 4, 3, 4, 3
train_file, test_file, tweet_model = "./data/Tweet_Train.txt", "./data/Tweet_Test.txt", "./output/tweet.model"

tweet_vocab = get_vocab(vocab_filename)
train_data = read_train_data(TRAIN, tweet_vocab, labels_map, train_text_index, train_label_index, delimiter='\t')
test_data = read_test_data(TEST, tweet_vocab, labels_map, test_text_index, test_label_index, delimiter='\t')

save_data(train_data, test_data, train_file, test_file)
print "Preprocess train and test data and output two files in SVM format: " + train_file + "\t" + test_file

## classify tweets ###############################
print os.system(svm_learn + " " + train_file + " " + tweet_model)
print "Created model ./output/tweet.model"
svm_output = "./output/svm_output.txt"
print os.system(svm_classify + " " + test_file + " " + tweet_model + " " + svm_output)
print "Output classifier result", svm_output

# classify tweets ###############################

# print os.system("python svm_postprocess.py")

# print os.system("python categorization.py")
#
# print os.system("python sentiment_analysis.py")

print ("Finished")