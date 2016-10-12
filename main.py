"""

"""
import os
import platform
from create_vocab_from_tweets import read_data, save_vocab_tweets, make_vocab
from svm_preprocess import get_vocab, read_train_data, read_test_data, save_data

# using proper library depends on OS type
platform = platform.system()
if platform == 'Windows':
    svm_learn = '.\lib\svm_learn.exe'
    svm_classify = '.\lib\svm_classify.exe'
else:
    svm_learn = './lib/svm_learn'
    svm_classify = './lib/svm_classify'

# merge crisislex datasets ###############################
# os.system("python process_crisislex.py")
# print "Created training data from CrisisLex26"


# create vocabulary ###############################
# input_filename = "./data/CL_training.csv"
# output_filename = "./data/CL_refined_training.csv"
input_filename = "./data/Ryan/training_tweets.txt"
output_filename = "./data/Ryan/refined_training_tweets.txt"
vocab_filename = "./data/Tweets.vocab"

refined_tweets, save_tweets = read_data(input_filename, tweet_index=4)
save_vocab_tweets(save_tweets, output_filename)
make_vocab(refined_tweets, vocab_filename)
print "Created refined traning data and vocabulary file"

# prepare training and testing inputs ###############################
# input_train_file="./data/CL_training.csv"
# input_test_file = "./data/tweets_hashtag.csv" # "./data/output/test.txt" #
input_train_file, input_test_file="./data/Ryan/training_tweets.txt", "./data/Ryan/testing_tweets.txt"
test_text_index, test_label_index, train_text_index, train_label_index = 4, 3, 4, 3
labels_map = {'Relevant':1, 'Not Relevant':-1}

train_file, test_file = "./data/Tweet_Train.txt", "./data/Tweet_Test.txt"

tweet_vocab = get_vocab(vocab_filename)
train_data = read_train_data(input_train_file, tweet_vocab, labels_map, train_text_index, train_label_index, delimiter='\t')
test_data = read_test_data(input_test_file, tweet_vocab, labels_map, test_text_index, test_label_index, delimiter='\t')

save_data(train_data, test_data, train_file, test_file)
print (
"Prerocess train and test data to output two corresponding files in SVM format: " + train_file + "\t" + test_file)

## classify tweets ###############################
print os.system(svm_learn + " ./data/Tweet_Train.txt ./output/tweet.model")
print "Created model ./output/tweet.model"
print os.system(svm_classify + " ./data/Tweet_Test.txt ./output/tweet.model ./output/svm_output.txt")
print "Output classifier result ./output/svm_output.txt"

# classify tweets ###############################

# print os.system("python svm_postprocess.py")

# print os.system("python categorization.py")
#
# print os.system("python sentiment_analysis.py")

print ("Finished")