# gensim modules
from gensim import utils
from gensim.models.doc2vec import LabeledSentence
from gensim.models import Doc2Vec

# numpy
import numpy

# shuffle
from random import shuffle

# logging
import logging
import os.path
import sys
import cPickle as pickle

from tweet_tokenizer import tokenize

program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)
logger.info("running %s" % ' '.join(sys.argv))

class LabeledLineSentence(object):

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
                    yield LabeledSentence(tokenize(line), [prefix + '_%s' % item_no])

    def to_array(self):
        self.sentences = []
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    self.sentences.append(LabeledSentence(
                        tokenize(line), [prefix + '_%s' % item_no]))
        return self.sentences

    def sentences_perm(self):
        shuffle(self.sentences)
        return self.sentences

# sources = {'./data/CrisisLex/test_not_related.txt':'TEST_NR', './data/CrisisLex/test_not_informative.txt':'TEST_NI', './data/CrisisLex/test_informative.txt':'TEST_IN', './data/CrisisLex/train_not_related.txt':'TRAIN_NR', './data/CrisisLex/train_not_informative.txt':'TRAIN_NI', './data/CrisisLex/train_informative.txt':'TRAIN_IN'}
sources = {'./data/CrisisLex/data/CrisisLexT6/2012_Sandy_Hurricane/on-topic.txt':'ON', './data/CrisisLex/data/CrisisLexT6/2012_Sandy_Hurricane/off-topic.txt':'OFF'}
sentences = LabeledLineSentence(sources)

model = Doc2Vec(min_count=1, window=10, size=100, sample=1e-4, negative=5, workers=10)

sentences_arr = sentences.to_array()
model.build_vocab(sentences_arr)

for epoch in range(50):
    logger.info('Epoch %d' % epoch)
    model.train(sentences.sentences_perm())

# model.save('./data/CrisisLex/CrisisLex.d2v')
model.save('./data/CrisisLex/2012_Sandy_Hurricane.d2v')