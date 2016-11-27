import numpy as np
import pandas as pd
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models, similarities
from sklearn import linear_model
from sklearn import cross_validation
from sklearn.metrics import roc_curve, auc
from sklearn import metrics
from scipy import interp
import sys
import json
from filter_new import clean_and_tokenize
import os.path
from sklearn import svm
import csv
import shlex
import subprocess

word2vec_flag = 0
model_flag = 0
day = [24,25,26,27,28,29,30,31]

neg_ratio = []

for j in day:
    if sys.argv[1] == "./data/CrisisLex/CrisisLex27K.csv":
        dimensions = int(sys.argv[2])
        df = pd.read_csv(sys.argv[1], encoding="ISO-8859-1", delimiter="\t")
        my_columns = ["id", "keyword", "key", "choose_one", "text"]
        df.columns = my_columns
        df['choose_one:confidence'] = df['choose_one'].map(
            lambda x: 1 if x == "Not related" or x == "Related and informative" else 0.5)
        df['choose_one'] = df['choose_one'].map(lambda
                                                    x: "Relevant" if x == "Related and informative" or x == "Related - but not informative" else "Not Relevant")

        if os.path.isfile('./data/word2vec/word_2_vec_token_mappings/crisislex26_stem_map_high.json'):
            stem_map_high = json.load(open('./data/word2vec/word_2_vec_token_mappings/crisislex26_stem_map_high.json'))
            stem_map_low = json.load(open('./data/word2vec/word_2_vec_token_mappings/crisislex26_stem_map_low.json'))
            low_2_high_map = json.load(open('./data/word2vec/word_2_vec_token_mappings/crisislex26_low_2_high_map.json'))

            word2vec_flag = 1

        if os.path.isfile('./model/crisis_model.lsi'):
            dictionary = corpora.Dictionary.load('./model/crisis_model.dict')
            tfidf = models.TfidfModel.load('./model/crisis_model.tfidf')
            lsi = models.LsiModel.load('./model/crisis_model.lsi')

            model_flag = 1


    elif sys.argv[1] == "./data/Ryan/10KLabeledTweets_confidence.csv":
        df = pd.read_csv(sys.argv[1], encoding="ISO-8859-1")
        dimensions = int(sys.argv[2])
        # load in the stored low_2_high_map
        if os.path.isfile('./data/word2vec/word_2_vec_token_mappings/ryan_stem_map_high.json'):
            stem_map_high = json.load(open('./data/word2vec/word_2_vec_token_mappings/ryan_stem_map_high.json'))
            stem_map_low = json.load(open('./data/word2vec/word_2_vec_token_mappings/ryan_stem_map_low.json'))
            low_2_high_map = json.load(open('./data/word2vec/word_2_vec_token_mappings/ryan_low_2_high_map.json'))

            word2vec_flag = 1

        if os.path.isfile('./model/model.lsi'):
            dictionary = corpora.Dictionary.load('./model/model.dict')
            tfidf = models.TfidfModel.load('./model/model.tfidf')
            lsi = models.LsiModel.load('./model/model.lsi')

            model_flag = 1

    input_file = "./data/state_id_2014-08-24/output/2014-08-"+str(j)+".txt"
    output_file = "./data/state_id_2014-08-24/output/2014-08-"+str(j)+"_hash_filter.txt"

    final_output_file = "./data/state_id_2014-08-24/output/2014-08-"+str(j)+"_sent.txt"

    type = int(sys.argv[3])     # type = 1 means filter by classification; otherwise, filter by hashtag


    if type == 1:

        df = df[["choose_one", "text", "choose_one:confidence"]]

        print "Total tweets: %d" % len(df)
        df = df.drop_duplicates(subset=["text"],
                                keep=False).reset_index()  # this also resets the index otherwise the numbers will have gaps
        print "Total unique tweets: %d" % len(df)

        df = clean_and_tokenize(df)

        # Loading the google word2vec dataset into the model


        # create a new column of tweets that are now mapped according to word2vec
        def map_low_frequency_tokens(split_tweet, low_2_high_map):
            split_tweet_return = []
            for token_stemmed in split_tweet:
                if token_stemmed in low_2_high_map:
                    split_tweet_return.append(low_2_high_map[token_stemmed])
                else:
                    split_tweet_return.append(token_stemmed)
            return split_tweet_return

        df["text_tokenized_stemmed_w2v"] = df["text_tokenized_stemmed"].apply(
            lambda x: map_low_frequency_tokens(x, low_2_high_map))

        # amount of tweets where words have been mapped
        print "Fraction of tweets mapped: %f" % (
        float(len(df[df['text_tokenized_stemmed'] != df['text_tokenized_stemmed_w2v']])) / float(len(df)))

        df_full = df[["choose_one", "text_tokenized_stemmed", "text_tokenized_stemmed_w2v"]]
        df_filtered = df[["choose_one", "text_tokenized_stemmed", "text_tokenized_stemmed_w2v"]][
            df["choose_one:confidence"] == 1].reset_index()

        print "# total tweets: %d" % len(df_full)
        print "# high certainty tweets: %d" % len(df_filtered)
        print "# lower certainty tweets: %d" % (len(df_full) - len(df_filtered))


        def k_fold_roc(df, dim, cross_val_num):
            # model used
            model = linear_model.LogisticRegression(class_weight="balanced", C=1)
            # model = linear_model.LogisticRegression()
            # create X and y data but need as a numpy array for easy cv ROC implementation
            # also need to usue dummies for the ROC curve so convert them en route
            X = pd.DataFrame.as_matrix(df[[i for i in range(dim)]])
            y = pd.get_dummies(df["choose_one"])["Relevant"]

            # create the cross validation entity to extract the dat from sequentially
            cv = cross_validation.StratifiedKFold(y, n_folds=cross_val_num)

            mean_tpr = 0.0
            mean_fpr = np.linspace(0, 1, 100)
            all_tpr = []

            roc_data = []
            for i, (train, test) in enumerate(cv):
                probas_ = model.fit(X[train], y[train]).predict_proba(X[test])

                fpr, tpr, thresholds = roc_curve(y[test], probas_[:, 1])
                mean_tpr += interp(mean_fpr, fpr, tpr)
                mean_tpr[0] = 0.0
                roc_auc = auc(fpr, tpr)

                roc_data.append([fpr, tpr, ('%d (area = %0.2f)' % (i, roc_auc))])

            mean_tpr /= len(cv)
            mean_tpr[-1] = 1.0
            mean_auc = auc(mean_fpr, mean_tpr)
            roc_data.append([mean_fpr, mean_tpr, ('Mean (area = %0.2f)' % mean_auc)])

            return roc_data


        def make_dictionary_and_corpus( df_corpus):
            # the tokenized and stemmed data form our texts database
            '''texts = df_dictionary'''

            # check how frequently a given word appears and remove it if only one occurrence
            '''frequency = defaultdict(int)
            for text in texts:
                for token in text:
                    frequency[token] += 1
            texts = [[token for token in text if frequency[token] > 1] for text in texts]'''

            # create a gensim dictionary
            #dictionary = corpora.Dictionary(texts)

            # create a new texts of only the ones I will analyze
            texts = df_corpus

            # create the bag of words corpus
            corpus = [dictionary.doc2bow(text) for text in texts]
            # corpus = [token_word2vec_map(text, frequency) for text in texts]

            # create a tfidf wrapper and convert the corpus to a tfidf format
            #tfidf = models.TfidfModel(corpus)
            corpus_tfidf = tfidf[corpus]

            # return a tuple with the dictionary and corpus
            return ( corpus_tfidf, corpus)


        tweet_type = "text_tokenized_stemmed"
        corpus_tfidf, corpus_bow = make_dictionary_and_corpus(df_filtered[tweet_type])



        def remove_doc_label(doc):
            cleaned_doc = []
            for element in doc:
                cleaned_doc.append(element[1])
            return cleaned_doc


        def latent_semantic_analysis(df, corpus_tfidf, return_topics=False, n_topics=10, n_words=10):
            # create a lsi wrapper around the tfidf wrapper
            #lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=dimensions, power_iters=10)
            corpus_lsi = lsi[corpus_tfidf]

            # create the features for a new dataframe
            features = []
            for doc in corpus_lsi:
                features.append(remove_doc_label(doc))

            # create a new dataframe with the features
            df_features = pd.DataFrame(data=features)

            # create a merged dataframe from the input (the indicies should match since I reset them earlier on)
            df_merged = pd.concat([df["choose_one"], df_features], axis=1)

            # return the new features dataframe devoid of columns that contain nothing
            if return_topics:
                return (df_merged.fillna(0), lsi.print_topics(n_topics, num_words=n_words), lsi)
            else:
                return df_merged.fillna(0)


        df_lsi_features, topics, lsi = latent_semantic_analysis(df_filtered, corpus_tfidf, True, 15, 20)

        cross_val_num = 8
        #roc_data = k_fold_roc(df_lsi_features, dimensions, cross_val_num)
        X = df_lsi_features[[i for i in range(dimensions)]]
        y = df_lsi_features["choose_one"]

        # split into test and train
        # print X
        X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, train_size=0.80)


        # make the model
        # model = linear_model.LogisticRegression(class_weight = "balanced", C = 1)
        #model = linear_model.LogisticRegression()
        model = svm.LinearSVC()
        model.fit(X_train, y_train)

        with open(input_file, 'rU') as f:
            rd = rd=csv.reader(f, delimiter=",")
            reader = []  # list of tweets

            for a in rd:
                arr = []
                # a = [x.strip() for x in line.split(',')]

                if len(a) > 5:
                    st = ""
                    for i in xrange(0, len(a) - 4):
                        if i == len(a) - 5:
                            st += a[i]
                        else:
                            st += a[i] + ", "
                    arr.append(st)
                    for i in xrange(len(a) - 4, len(a)):
                        arr.append(a[i])
                    a = []
                    a = arr
                reader.append(a)
        reader = pd.DataFrame(reader)
        my_columns = ["text", "time", "id", "lat", "log"]
        reader.columns = my_columns

        reader = reader.drop_duplicates(subset=["text"],
                                keep=False).reset_index()
        reader = clean_and_tokenize(reader)

        test_tweet_type = "text_tokenized_stemmed"
        test_corpus_tfidf, test_corpus_bow = make_dictionary_and_corpus(reader[test_tweet_type])

        def test_latent_semantic_analysis(df, corpus_tfidf, return_topics=False, n_topics=10, n_words=10):
            # create a lsi wrapper around the tfidf wrapper
            #lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=dimensions, power_iters=10)
            corpus_lsi = lsi[corpus_tfidf]

            # create the features for a new dataframe
            features = []
            for doc in corpus_lsi:
                features.append(remove_doc_label(doc))

            # create a new dataframe with the features
            df_features = pd.DataFrame(data=features)



            # create a merged dataframe from the input (the indicies should match since I reset them earlier on)
            df_merged = pd.concat([df, df_features], axis=1)
            #[df["choose_one"], df_features]

            # return the new features dataframe devoid of columns that contain nothing
            if return_topics:
                return (df_merged.fillna(0), lsi.print_topics(n_topics, num_words=n_words), lsi)
            else:
                return df_merged.fillna(0)
        #print reader

        test_df_lsi_features, test_topics, test_lsi = test_latent_semantic_analysis(reader, test_corpus_tfidf, True, 15, 20)



        test_X = test_df_lsi_features[[i for i in range(dimensions)]]


        #print test_X
        test_y_pred = model.predict(test_X)



        xyz = test_df_lsi_features[["text", "time", "id", "lat", "log"]]
        with open(output_file, "wb") as f2:
            s = []
            j = 0
            for index, row in xyz.iterrows():
                if test_y_pred[j] == "Relevant":
                    s = str(row['text'])+", "+str(row['time'])+", "+str(row['id'])+", "+str(row['lat'])+", "+str(row['log'])
                    f2.write(s + '\n')
                j += 1


        y_pred = model.predict(X_test)



        # various "fitness" metrics
        print "Train accuracy: %f \n" % model.score(X_train, y_train)
        print "Test accuracy: %f \n" % model.score(X_test, y_test)
        print "F1 score: %f \n" % metrics.f1_score(y_test, y_pred, labels=None, pos_label='Relevant', average='binary',
                                                   sample_weight=None)

        # confusion matrix
        cm = metrics.confusion_matrix(y_test, model.predict(X_test))
        print "Confusion matrix: \n"
        print "-Legend"
        print np.array([['True "not disaster"', 'False "disaster"'], ['False "not disaster"', 'True "disaster"']])
        print "\n-Prediction"
        print cm

        print "\n-Precision"
        print cm[1][1] / ((cm[1][1] + cm[0][1]) * 1.0)

        print "\n-Recall"
        print cm[1][1] / ((cm[1][0] + cm[1][1]) * 1.0)
        print "\n"

    else:   # filter disaster-related tweets using hashtags

        import re

        r = re.compile(
            r'napaearthquake | earthquake | quake | southnapaquake | napa | napaquake | americancanyon  | earthquakeamericancanyon | bayareaquake | sfearthquake | naturaldisaster | earthquakeamericancanyon',
            flags=re.I | re.X)
        disaster_tweets_count = 0
        with open(input_file) as f:
            with open(output_file, "wb") as f2:
                for line in f:
                    arr = []
                    a = [x.strip() for x in line.split(',')]

                    if len(a) > 5:
                        st = ""
                        for i in xrange(0, len(a) - 4):
                            if i == len(a) - 5:
                                st += a[i]
                            else:
                                st += a[i] + ", "
                        arr.append(st)
                        for i in xrange(len(a) - 4, len(a)):
                            arr.append(a[i])
                        a = []
                        a = arr
                    if re.search(r, a[0]):
                        # print a[0]
                        f2.write(', '.join(a) + '\n')
                        disaster_tweets_count += 1
        print "Disaster related tweets: ", disaster_tweets_count



    def SentiStrength(tweet):
        #open a subprocess using shlex to get the command line string into the correct args list format
        p = subprocess.Popen(shlex.split("java -jar SentiStrength.jar stdin sentidata data/SentStrength_Data/ trinary"),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        #communicate via stdin the string to be rated. Note that all spaces are replaced with +
        #stdout_text, stderr_text = p.communicate(tweet.replace(" ", "+").encode())
        stdout_text, stderr_text = p.communicate(tweet.replace(" ", "+"))
        #remove the tab spacing between the positive and negative ratings. e.g. 1    -5 -> 1-5
        stdout_text = stdout_text.rstrip().decode().replace("\t","")
        return stdout_text


    """
    run senstiment analysis for a file, including a set of tweets
    each line of input file is a tweet's information
    tweet_index is the index of the text in each line
    """

    def sensiment_analyzer(tweet_input, tweet_output, delimiter=',', tweet_index=0):
        moods=[]
        qw = 0
        count_pos = 0
        count_neg = 0
        mood_stats = {}  # counting frequency of tweet
        with open(tweet_input, 'rU') as f:
            with open(tweet_output, "wb") as f2:
                rd=csv.reader(f, delimiter=delimiter)
                reader=[]   # list of tweets
                for a in rd:
                    arr = []
                    #a = [x.strip() for x in line.split(',')]

                    if len(a) > 5:
                        st = ""
                        for i in xrange(0, len(a) - 4):
                            if i == len(a) - 5:
                                st += a[i]
                            else:
                                st += a[i] + ", "
                        arr.append(st)
                        for i in xrange(len(a) - 4, len(a)):
                            arr.append(a[i])
                        a = []
                        a = arr

                    res=SentiStrength(a[tweet_index])
                    mood = int(res.split()[2])
                    moods.append(mood)
                    if mood == -1:
                        count_neg += 1
                    elif mood == 1:
                        count_pos += 1

                    a.append(str(mood))
                    #print a
                    f2.write(', '.join(a) + '\n')
                    qw += 1
                    if qw % 20 == 0:
                        print 'Processed tweets: ' + str(qw)

        print "neg =", count_neg
        print "pos = ", count_pos
        print (count_neg / ((count_pos + count_neg) * 1.0))
        print (count_neg / (qw * 1.0))

        neg_ratio.append(count_neg / ((count_pos + count_neg) * 1.0))

    sensiment_analyzer(output_file, final_output_file, ',', 0)


"""
Daily plot
"""
import matplotlib.pyplot as plt
#plt.plot([0.43, 0.39, 0.42, 0.23, 0.17, 0.13, 0.17, 0.24])
plt.plot(neg_ratio)
plt.ylabel('neg_ratio')
plt.xlabel('day')
plt.show()



"""
Hourly plot
"""
import time
import datetime

s = "2014-08-24 06:00:00"
s_time = time.mktime(datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S").timetuple())
arr = []
for k in xrange(1,8):
    pos = 0
    neg = 0
    total = 0
    set_time = s_time + k*10800
    with open("./data/state_id_2014-08-24/output/2014-08-24_sent.txt") as f2:
        for i in f2:
            a = [x.strip() for x in i.split(',')]
            t = time.mktime(datetime.datetime.strptime(a[1], "%Y-%m-%d %H:%M:%S").timetuple())
            if set_time > int(t) and int(t) > set_time - 10800:
                if int(a[5]) == -1:
                    neg += 1
                elif int(a[5]) == 1:
                    pos += 1
                total += 1
        if pos == 0:
            arr.append(0)
        else:
            arr.append(neg / ((pos + neg) * 1.0))

        print neg, pos, total
import matplotlib.pyplot as plt
plt.plot(arr)
plt.ylabel('neg_ratio')
plt.xlabel('hour')
plt.show()