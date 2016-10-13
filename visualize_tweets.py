 # gensim modules
from gensim import utils
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec
from sklearn.manifold import TSNE

# random shuffle
from random import shuffle

# numpy
import numpy as np

# classifier
from sklearn.linear_model import LogisticRegression

import logging
import sys

# plotting lib
import graph_plot

log = logging.getLogger()
log.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)


# model = Doc2Vec.load('./data/CrisisLex/CrisisLex.d2v')
model = Doc2Vec.load('./data/CrisisLex/2012_Sandy_Hurricane.d2v')


# labels_count = {'TEST_NR':878, 'TEST_NI':1068, 'TEST_IN':3508, 'TRAIN_NR':1984, 'TRAIN_NI':6664, 'TRAIN_IN':13341}
# labels_count = {'TEST_NR':878, 'TEST_NI':1068, 'TEST_IN':3508}
labels_count = {'ON':4803, 'OFF':3192}

# labels = {'TEST_NR':-1, 'TEST_NI':1, 'TEST_IN':1, 'TRAIN_NR':-1, 'TRAIN_NI':0, 'TRAIN_IN':1}
labels = {'ON':1, 'OFF':0}
# TRAIN_SIZE = labels_count['TRAIN_NR'] + labels_count['TRAIN_NI'] + labels_count['TRAIN_IN']
# TEST_SIZE = labels_count['TEST_NR'] + labels_count['TEST_NI'] + labels_count['TEST_IN']
SIZE = np.sum([count for count in labels_count.values()])
data = np.zeros((SIZE, 200))
data_labels = np.zeros(SIZE)

# compute data and corresponding labels
pos = 0
for prefix, count in labels_count.items():
    for i in range(count):
        prefix_index = prefix + '_' + str(i)
        data[pos] = model.docvecs[prefix_index]
        data_labels[pos] = labels[prefix]
        pos = pos + 1

# run t-SNE
tsne_model = TSNE(n_components=2, random_state=0, n_iter=1000)
Y = tsne_model.fit_transform(data)

# annotations = data_labels
graph_plot.dump_graph(Y, data_labels, './data/CrisisLex/t-sne', None, 2)