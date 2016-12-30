 # gensim modules
from gensim import utils
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec
import os.path
from tweet_tokenizer import tokenize
from Params import Params

# random shuffle
from random import shuffle

# numpy
import numpy

# classifier
from sklearn.linear_model import LogisticRegression

import logging
import sys

log = logging.getLogger()
log.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)

class TaggedLineSentence(object):
    def __init__(self, sources):
        self.sources = sources

        flipped = {}

        # make sure that keys are unique
        for key, value in sources.items():
            if value not in flipped:
                flipped[value] = [key]
            else:
                raise Exception('Non-unique prefix encountered')

    def __iter__(self):
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    yield TaggedDocument(utils.to_unicode(line).split(), [prefix + '_%s' % item_no])

    def to_array(self):
        self.sentences = []
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    self.sentences.append(TaggedDocument(utils.to_unicode(line).split(), [prefix + '_%s' % item_no]))
        return self.sentences

    def sentences_perm(self):
        shuffle(self.sentences)
	return self.sentences
        

log.info('source load')
sources = {'test-neg.txt':'TEST_NEG', 'test-pos.txt':'TEST_POS', 'train-neg.txt':'TRAIN_NEG', 'train-pos.txt':'TRAIN_POS'}

log.info('TaggedDocument')
# sentences = TaggedLineSentence(sources)
#
# log.info('D2V')
# model = Doc2Vec(min_count=1, window=10, size=100, sample=1e-4, negative=5, workers=7)
# model.build_vocab(sentences.to_array())
#
# log.info('Epoch')
# for epoch in range(10):
# 	log.info('EPOCH: {}'.format(epoch))
# 	model.train(sentences.sentences_perm())
#
# log.info('Model Save')
# model.save('./imdb.d2v')

model = Doc2Vec.load('./model/word2vec-sentiments-master/tweets.d2v')

"""
training the model on a doc2vec dataset, output a classifier
"""
def train():
    log.info('Sentiment')
    train_arrays, train_labels = numpy.zeros((800000*2, 100)), numpy.zeros(800000*2)

    # put the positive ones at the first half of the array, and the negative ones at the second half
    for i in range(800000):
        prefix_train_pos, prefix_train_neg = 'TRAIN_POS_' + str(i), 'TRAIN_NEG_' + str(i)
        train_arrays[i], train_arrays[800000 + i] = model.docvecs[prefix_train_pos], model.docvecs[prefix_train_neg]
        train_labels[i], train_labels[800000 + i] = 1, -1

    log.info('Fitting')
    classifier = LogisticRegression()
    classifier.fit(train_arrays, train_labels)
    LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
              intercept_scaling=1, penalty='l2', random_state=None, tol=0.0001)
    return classifier

# print train_labels


# tweet datasets for prediction
"""
predict sentiment for a list of disasters, identified by disasters_ids
output a set of coresponding files of labels
"""
PREDICTING = False
# N = 16342   # Napa
# N = 2067    # michigan flood (affected)
# N = 121093    # michigan flood (unaffected)
if PREDICTING:
    # training
    classifier = train()
    """
    for all disasters, and all kinds of data, e.g., (un)affected, (un)filtered
    """
    for disaster_id in Params.disaster_ids:
        for affect in ['_affected', '_unaffected']:
            for filter in ['_filtered']:
                value = disaster_id + affect + filter
                file = Params.tweet_folder + value + '.txt'
                if os.path.isfile(file):
                    tweet_count = sum(1 for line in open(file)) # count the number of tweets in file
                    print file, tweet_count
                    predict_arrays = [ model.docvecs[value + '_' + str(i)] for i in range(tweet_count)]

                    # predicting
                    LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
                              intercept_scaling=1, penalty='l2', random_state=None, tol=0.0001)
                    labels = classifier.predict(predict_arrays)
                    numpy.savetxt(Params.label_folder + value + '.txt', labels, delimiter='\t')

if False:
    # training
    classifier = train()
    """
    for all disasters, and all kinds of data, e.g., (un)affected, (un)filtered
    """
    for disaster_id in Params.disaster_ids:
        for affect in ['_affected', '_unaffected']:
            for filter in ['_filtered', '_unfiltered']:
                value = disaster_id + affect + filter
                file = './model/word2vec-sentiments-master/tweets_unaffected_unfiltered/' + value + '.txt'
                if os.path.isfile(file):
                    tweet_count = sum(1 for line in open(file)) # count the number of tweets in file
                    predict_arrays = [model.docvecs[value + '_' + str(i)] for i in range(tweet_count)]
                    # predicting
                    LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
                              intercept_scaling=1, penalty='l2', random_state=None, tol=0.0001)
                    labels = classifier.predict(predict_arrays)
                    pos = labels.tolist().count(1)
                    neg = len(labels) - pos
                    print value, pos, neg
                    numpy.savetxt('./model/word2vec-sentiments-master/tweets_unaffected_unfiltered/labels/' + value + '.txt', labels, delimiter='\t')

# classifier = train()
# file = './model/word2vec-sentiments-master/predict.txt'
# tweet_count = sum(1 for line in open(file)) # count the number of tweets in file
# print file, tweet_count
# predict_arrays = numpy.zeros((tweet_count, 100))
#
# for i in range(tweet_count):
#     prefix_predict = 'PREDICT_' + str(i)
#     predict_arrays[i] = model.docvecs[prefix_predict]
#
# # predicting
# LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
#           intercept_scaling=1, penalty='l2', random_state=None, tol=0.0001)
# labels = classifier.predict(predict_arrays)
# pos = sum([1 for i in labels if i == 1])
# neg = sum([1 for i in labels if i == -1])
# print pos, neg
# numpy.savetxt('./model/word2vec-sentiments-master/predict_labels.txt', labels, delimiter='\t')


TESTING = True
if TESTING:
    test_arrays = numpy.zeros((182+177, 100))
    test_labels = numpy.zeros(182+177)

    for i in range(182):
        test_arrays[i] = model.docvecs['TEST_POS_' + str(i)]
        test_labels[i] = 1

    for i in range(177):
        test_arrays[182 + i] = model.docvecs['TEST_NEG_' + str(i)]
        test_labels[182 + i] = -1

    classifier = train()
    LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
              intercept_scaling=1, penalty='l2', random_state=None, tol=0.0001)
    print classifier.score(test_arrays, test_labels)