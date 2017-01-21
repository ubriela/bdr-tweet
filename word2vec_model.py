import numpy as np
import pandas as pd
from collections import defaultdict
from nltk.tokenize import TweetTokenizer
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models, similarities
from sklearn import linear_model
from sklearn import cross_validation
from sklearn.metrics import roc_curve, auc
from sklearn import metrics
from scipy import interp
import matplotlib.pyplot as plt
import sys
import json


#These are special modules that I built to streamline parsing, tokenization and the LSI step

from latent_semantic_indexing import latent_semantic_indexer


# Converting the csv file to dataframe with column names.

input_file = "./data/disasters/classify/fire_flood.csv"
dimensions = 100
arr = []
with open(input_file) as f:
    for line in f:
        a = [x.strip() for x in line.split(',')]
        arr.append(a)

#df = np.array(arr)
#df = pd.read_csv(input_file, encoding="ISO-8859-1", delimiter=",")
my_columns = ["choose_one", "text", "none"]

df = pd.DataFrame(arr, columns=my_columns)
df['choose_one:confidence'] = df['choose_one'].map(lambda x: 1 if x == "Not Relevant" or x == "Relevant" else 0.5)

#print df
#load in the stored low_2_high_map
#stem_map_high = json.load(open('./data/word2vec/word_2_vec_token_mappings/crisislex26_stem_map_high.json'))
#stem_map_low = json.load(open('./data/word2vec/word_2_vec_token_mappings/crisislex26_stem_map_low.json'))
#low_2_high_map = json.load(open('./data/word2vec/word_2_vec_token_mappings/crisislex26_low_2_high_map.json'))



    #dictionary = corpora.Dictionary.load('./model/model.dict')
    #print dictionary

# Creating a column name called choose_one:confidence and assigning 1 or 0.5 score to it.


# Only keep the columns relevant to this work
df = df[["choose_one", "text", "choose_one:confidence"]]

# removing the duplicate tweets

print "Total tweets: %d" % len(df)
df = df.drop_duplicates(subset = ["text"], keep=False).reset_index() #this also resets the index otherwise the numbers will have gaps
print "Total unique tweets: %d" % len(df)


def utf8_to_ascii(tweet):
    utf8_hyphens = "\xe2\x80\x90 \xe2\x80\x91 \xe2\x80\x92 \xe2\x80\x93 \xe2\x80\x94".split()
    utf8_aposts = "\xe2\x80\x98 \xe2\x80\x99 \xe2\x80\x9b \xe2\x80\xb2 \xe2\x80\xb5".split()
    return_tweet = tweet.decode('utf-8')
    for utf8_hyphen in utf8_hyphens:
        return_tweet = return_tweet.replace(utf8_hyphen, "-")
    for utf8_apost in utf8_aposts:
        return_tweet = return_tweet.replace(utf8_apost, "'")
    return return_tweet


# breaks up tags assuming a common format of words with no spacing denoted by capitalization (i.e. CrazyDay or JohnDoe)
def break_tag(tag):
    broken_tag = []
    word = ""
    for letter in tag:
        if letter.isupper():
            if word:
                broken_tag.append(word)
            word = letter[:]
        else:
            word = word + letter
    broken_tag.append(word)
    return broken_tag


# function to break up any tags or handles into words if in a normal format
# clean up hash tags which can contain useful information
def clean_tags(split_tweet):
    split_tweet_return = []
    for entry in split_tweet:
        if (entry[0] == "@" and len(entry) > 1):
            split_tweet_return.append("@")
            split_tweet_return.append(entry[1:])
        elif (entry[0] == "#" and len(entry) > 1):
            split_tweet_return.append("#")
            for tag_comp in break_tag(entry[1:]):
                split_tweet_return.append(tag_comp)
        else:
            split_tweet_return.append(entry)
    return split_tweet_return


# go through and label any numeric entries as a special numeric token
def num_token(split_tweet):
    num = "0 1 2 3 4 5 6 7 8 9 ,".split()
    split_tweet_return = []
    for entry in split_tweet:
        if entry == ",":
            split_tweet_return.append(entry)
        else:
            is_other = False
            for char in entry:
                if char not in num:
                    is_other = True
                    break
            if is_other:
                split_tweet_return.append(entry)
            else:
                split_tweet_return.append("|-num-|")
    return split_tweet_return


# go through and label any mixed number and letter entries as a special numalpha token
# make sure that this does not label anything as num_alpha that came from a handle (which is common)
def num_alpha_token(split_tweet):
    num = "0 1 2 3 4 5 6 7 8 9".split()
    alpha = "a b c d e f g h i j k l m n o p q r s t u v w x y z".split()
    split_tweet_return = []
    prior_entry = ""
    for entry in split_tweet:
        has_num = False
        has_alpha = False
        has_other = False
        for char in entry:
            if char in num:
                has_num = True
            elif char in alpha:
                has_alpha = True
            else:
                has_other = True
        if (has_num and has_alpha and not has_other and (prior_entry != "@")):
            split_tweet_return.append("|-num_alpha-|")
        else:
            split_tweet_return.append(entry)
        prior_entry = entry[:]
    return split_tweet_return


# go through and label any numeric words with special tokens
def word_num_token(split_tweet):
    units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    scales = ["hundred", "thousand", "million", "billion", "trillion"]
    split_tweet_return = []
    for entry in split_tweet:
        if entry in units:
            split_tweet_return.append("|-num_units-|")
        elif entry in tens:
            split_tweet_return.append("|-num_tens-|")
        elif entry in scales:
            split_tweet_return.append("|-num_scales-|")
        else:
            split_tweet_return.append(entry)
    return split_tweet_return


# tokenize a web address if present
def website_tokenize(split_tweet):
    split_tweet_return = []
    for entry in split_tweet:
        if entry[0:4] == "http":
            split_tweet_return.append("|-website-|")
        else:
            split_tweet_return.append(entry)
    return split_tweet_return


# determines if the token is likely an emoticon and if so returns a reduced representation
# the reduced representation is to aid in statistics since the eyes and mouth really convey
# emotions with minimal information included from a nose or something else
def is_emoji(token):
    # these features make up most smileys which is ~90% of all emojis
    # faces will be returned all facing the right ala eyes then mouth
    eyes = ": ; = 8"
    mouth = "( ) [ ] d p { } / @ |"
    found_eyes = False
    found_mouth = False
    emoji = ""
    for char in token:
        if (char in eyes and not found_eyes):
            emoji = emoji + char
            found_eyes = True
        if (char in mouth and not found_mouth):
            emoji = emoji + char
            found_mouth = True
    # flip all emojis to face normal direction if needed
    if (found_eyes and found_mouth):
        if emoji[0] in mouth:
            e_mouth = emoji[0]
            e_eyes = emoji[1]
            emoji = ""
            emoji = emoji + e_eyes
            if e_mouth == "(":
                emoji = emoji + ")"
            elif e_mouth == ")":
                emoji = emoji + "("
            elif e_mouth == "[":
                emoji = emoji + "]"
            elif e_mouth == "]":
                emoji = emoji + "["
            # this one is unique as it has a directionality so only need one check
            elif e_mouth == "d":
                emoji = emoji + "p"
            elif e_mouth == "{":
                emoji = emoji + "}"
            elif e_mouth == "}":
                emoji = emoji + "{"
            else:
                emoji = emoji + e_mouth
        return emoji
    else:
        return token

        # function to check common happy face tweets and reduce them down to only eyes and a mouth


# these are the dominant features that imply emotion
def downgrade_emoji(split_tweet):
    split_tweet_return = []
    for entry in split_tweet:
        split_tweet_return.append(is_emoji(entry))
    return split_tweet_return


#function to clean and tokenize the tweets all in one fell swoop
#needed function definitions are defined immediately above

def clean_and_tokenize(df):
    #convert some common utf8 hyphen and apostrophe symbols to ascii
    #df["text"] = df["text"].apply(utf8_to_ascii)
    #go through and convert or remove any remaining utf8 characters
    #df["text"] = df["text"].apply(lambda(tweet): tweet.decode("utf8").encode('ascii',  errors='replace'))
    #clean up any html tags
    #html_parser = HTMLParser.HTMLParser()
    #df["text"] = df["text"].apply(html_parser.unescape)
    #split text on hypenations
    #df["text"] = df["text"].apply(lambda(tweet): tweet.replace("-", " "))
    #start out tokenization using NLTK casual twitter token (store in text_tokenized)
    tknzr = TweetTokenizer(strip_handles=False, reduce_len=True)
    df["text_tokenized"] = df["text"].apply(tknzr.tokenize)
    #split up the tags
    df["text_tokenized"] = df["text_tokenized"].apply(clean_tags)
    #lowercase everything
    df["text_tokenized"] = df["text_tokenized"].apply(lambda(split_tweet): [entry.lower() for entry in split_tweet])
    #tokenize numbers
    df["text_tokenized"] = df["text_tokenized"].apply(num_token)
    #tokenize mixed alphabetical and numeric entries
    df["text_tokenized"] = df["text_tokenized"].apply(num_alpha_token)
    #tokenize any words that are numbers into base units, tens, and scales
    df["text_tokenized"] = df["text_tokenized"].apply(word_num_token)
    #tokenize website links
    df["text_tokenized"] = df["text_tokenized"].apply(website_tokenize)
    #actually modify the emojis
    df["text_tokenized"] = df["text_tokenized"].apply(downgrade_emoji)
    #go through and stem everything using the Porter Stemmer
    st = PorterStemmer()
    df["text_tokenized_stemmed"] = df["text_tokenized"].apply(lambda(split_tweet): [st.stem(entry) for entry in split_tweet])
    #send back the modified dataframe
    return df

df = clean_and_tokenize(df)

# Loading the google word2vec dataset into the model
w2v_model = models.word2vec.Word2Vec.load_word2vec_format('./data/word2vec/GoogleNews-vectors-negative300.bin.gz', binary=True)


# create the actual mapping dictionary for the low frequency words
def create_low_2_high_map(stem_map_low, stem_map_high):
    # loop over the low stemmed tokens and find a mapping to a high for each
    print "Creating low-to-high frequency token mapping via word2vec:"
    print "Number of low frequency tokens to map: %d" % len(stem_map_low)
    print "Number of high frequency tokens to choose from: %d" % len(stem_map_high)
    iteration = 0
    low_2_high_map = {}
    for low_token_stemmed in stem_map_low:
        sys.stdout.write('\r' + "Mapping token number =  " + ("%d" % iteration))
        low_token = stem_map_low[low_token_stemmed][0]  # only one entry for each low token
        # find the most similar high stemmed token
        max_similarity = 0.0
        max_high_token_stemmed = ""
        for high_token_stemmed in stem_map_high:
            for high_token in stem_map_high[high_token_stemmed]:
                try:
                    similarity_1 = w2v_model.similarity(low_token, high_token)
                except:
                    similarity_1 = -1.0
                try:
                    similarity_2 = w2v_model.similarity(low_token.title(), high_token)
                except:
                    similarity_2 = -1.0
                try:
                    similarity_3 = w2v_model.similarity(low_token, high_token.title())
                except:
                    similarity_3 = -1.0
                try:
                    similarity_4 = w2v_model.similarity(low_token.title(), high_token.title())
                except:
                    similarity_4 = -1.0

                similarity = max([similarity_1, similarity_2, similarity_3, similarity_4])

                if similarity > max_similarity:
                    max_similarity = similarity
                    max_high_token_stemmed = high_token_stemmed

        if max_high_token_stemmed:
            low_2_high_map[low_token_stemmed] = max_high_token_stemmed
        else:
            low_2_high_map[low_token_stemmed] = "|-no_w2v-|"
        iteration = iteration + 1
    return low_2_high_map


# removes doubles of a any token entry
def remove_clones(token_list):
    token_list_cleaned = []
    for token in token_list:
        if token not in token_list_cleaned:
            token_list_cleaned.append(token)
    return token_list_cleaned


# initialize the mapping of low frequency words onto high frequency words
def create_token_mappings(df):
    # create a stemmed word to full word map to use with word2vec
    # make sure to only use words for the mapping so check if only alphabetical characters
    print "Creating fundamental token map"
    st = PorterStemmer()
    texts = df["text_tokenized"]
    stem_map = {}
    for text in texts:
        for token in text:
            if is_word(token):
                token_stemmed = st.stem(token)
                if token_stemmed in stem_map:
                    stem_map[token_stemmed].append(token)
                else:
                    stem_map[token_stemmed] = [token]

    # create separate high frequency (>1 occurence) and low frequency (=1) stemmmed-unstemmed maps
    print "Separating into high and low frequency maps"
    stem_map_high = {}
    stem_map_low = {}
    for token_stemmed in stem_map:
        token_list = stem_map[token_stemmed]
        if len(token_list) > 1:
            stem_map_high[token_stemmed] = remove_clones(token_list)
        else:
            stem_map_low[token_stemmed] = token_list

    # create a mapping from the low stems to a suitable high stem using word2vec to calculate similarities
    # between the underlying unstemmed words contained in each
    low_2_high_map = create_low_2_high_map(stem_map_low, stem_map_high)

    return (stem_map_high, stem_map_low, low_2_high_map)


# this actually loops through and replaces all of the low frequency stemmed tokens with the high frequency analogs
def map_low_frequency_tokens(split_tweet, low_2_high_map):
    split_tweet_return = []
    for token_stemmed in split_tweet:
        if token_stemmed in low_2_high_map:
            split_tweet_return.append(low_2_high_map[token_stemmed])
        else:
            split_tweet_return.append(token_stemmed)
    return split_tweet_return


# checks of a token is likely a word
def is_word(token):
    alpha = "a b c d e f g h i j k l m n o p q r s t u v w x y z".split()
    for char in token:
        if ((char not in alpha) and (char != "'")):
            return False
    return True



#make the mapping for low frequecy words and write to a json file for safe keeping
stem_map_high, stem_map_low, low_2_high_map = create_token_mappings(df[["text_tokenized","text_tokenized_stemmed"]])
with open('./data/disasters/classify/fire_flood_low_2_high_map.json', 'w') as fp:
    json.dump(low_2_high_map, fp)
with open('./data/disasters/classify/fire_flood_stem_map_high.json', 'w') as fp:
    json.dump(stem_map_high, fp)
with open('./data/disasters/classify/fire_flood_stem_map_low.json', 'w') as fp:
    json.dump(stem_map_low, fp)




#create a new column of tweets that are now mapped according to word2vec
df["text_tokenized_stemmed_w2v"] = df["text_tokenized_stemmed"].apply(lambda x: map_low_frequency_tokens(x, low_2_high_map))

#amount of tweets where words have been mapped
print "Fraction of tweets mapped: %f" % (float(len(df[df['text_tokenized_stemmed'] != df['text_tokenized_stemmed_w2v']])) / float(len(df)))


# makes the gensim dictionary and corpus
def make_dictionary_and_corpus(df_dictionary, df_corpus):
    # the tokenized and stemmed data form our texts database
    texts = df_dictionary

    # check how frequently a given word appears and remove it if only one occurrence
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1
    texts = [[token for token in text if frequency[token] > 1] for text in texts]

    # create a gensim dictionary
    dictionary = corpora.Dictionary(texts)

    # create a new texts of only the ones I will analyze
    texts = df_corpus

    # create the bag of words corpus
    corpus = [dictionary.doc2bow(text) for text in texts]
    # corpus = [token_word2vec_map(text, frequency) for text in texts]

    # create a tfidf wrapper and convert the corpus to a tfidf format
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    # return a tuple with the dictionary and corpus
    return (dictionary, corpus_tfidf, corpus, tfidf)


# clean the features for use in dataframe
def remove_doc_label(doc):
    cleaned_doc = []
    for element in doc:
        cleaned_doc.append(element[1])
    return cleaned_doc


# takes as input the tweet dataframe, dictionary, corpus and dimensions for the tweets and returns
# a new dataframe with each tweet characterized by the new lower dimensional features
# also returns the topics if desired
def latent_semantic_analysis(df, dictionary, corpus_tfidf, dimensions, return_topics=False, n_topics=10, n_words=10):
    # create a lsi wrapper around the tfidf wrapper
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=dimensions, power_iters=5)
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

#create separate full and dictionary dataframes
df_full = df[["choose_one","text_tokenized_stemmed","text_tokenized_stemmed_w2v"]]
df_filtered = df[["choose_one","text_tokenized_stemmed","text_tokenized_stemmed_w2v"]][df["choose_one:confidence"] == 1].reset_index()
#df_filtered = df_full


#generate the dictionary and the corpus for our tweets
tweet_type = "text_tokenized_stemmed_w2v"
dictionary, corpus_tfidf, corpus_bow, tfidf = make_dictionary_and_corpus(df_full[tweet_type], df_filtered[tweet_type])

dictionary.save('./data/disasters/classify/fire_flood_model.dict')
tfidf.save('./data/disasters/classify/fire_flood_model.tfidf')

print "# total tweets: %d" % len(df_full)
print "# high certainty tweets: %d" % len(df_filtered)
print "# lower certainty tweets: %d" % (len(df_full)-len(df_filtered))


def score_across_dim(df, dictionary, corpus_tfidf, power, samples, cross_val_num):
    # select model
    model = linear_model.LogisticRegression(class_weight="auto")

    # list for returning dimensions
    dimensions_used = np.unique(np.logspace(0, power, num=samples, endpoint=True, base=10.0, dtype=int))

    # list for returning the average score from k-fold validation
    scores_cv = []
    scores_absolute = []

    # loop over the dimensions for performing the k-fold validation
    for dimensions in dimensions_used:
        # calculate model dataframe
        df_model = latent_semantic_analysis(df, dictionary, corpus_tfidf, dimensions)
        # actual validation
        scores = cross_validation.cross_val_score(model,
                                                  df_model[[i for i in range(dimensions)]],
                                                  df_model["choose_one"],
                                                  cv=cross_val_num)
        # compute average score
        scores_cv.append(np.average(scores))

        # create the vectors for fitting
        X = df_model[[i for i in range(dimensions)]]
        y = df_model["choose_one"]
        # fit the model
        model.fit(X, y)
        # compute score
        scores_absolute.append(model.score(X, y))

        # print out current dimensionality
        sys.stdout.write('\r' + "Calculating fit for dimensions = " + ("%d" % dimensions))

    return (dimensions_used, scores_cv, scores_absolute)

#w2v fitting
dimensions_used, scores_cv, scores_absolute = score_across_dim(df_filtered, dictionary, corpus_tfidf, 3, 100, 8)

#write out the cv data to a file
scores_df = pd.DataFrame(zip(dimensions_used, scores_cv, scores_absolute), columns = ["dimensions_used", "scores_cv", "scores_absolute"])
scores_df.to_csv("./output/score_data.csv")

max_score = 0
for entry in zip(scores_cv, dimensions_used):
    if entry[0] > max_score:
        max_score = entry[0]
        max_d = entry[1]
print (max_score, max_d)



#dimensions = 300
new_dimensions = 750
print len(dictionary)
print len(df_filtered)
df_lsi_features, topics, lsi = latent_semantic_analysis(df_filtered, dictionary, corpus_tfidf, new_dimensions, True, 15, 10)

lsi.save('./data/disasters/classify/fire_flood_model.lsi')


# so a dimensionality of ~100 seems perfectly fine... lets use this dimensionality and create a k-fold ROC curve
def k_fold_roc(df, dim, cross_val_num):
    # model used
    model = linear_model.LogisticRegression()

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

cross_val_num = 8
roc_data = k_fold_roc(df_lsi_features, dimensions, cross_val_num)

#make the X and y
X = df_lsi_features[[i for i in range(dimensions)]]
y = df_lsi_features["choose_one"]

#split into test and train
#print X
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, train_size=0.80)

#make the model
model = linear_model.LogisticRegression()
model.fit(X_train, y_train)
#print X_test
y_pred = model.predict(X_test)
#print y_pred
#various "fitness" metrics
print "Train accuracy: %f \n" % model.score(X_train, y_train)
print "Test accuracy: %f \n" % model.score(X_test, y_test)
print "F1 score: %f \n" % metrics.f1_score(y_test, y_pred, labels=None, pos_label='Relevant', average='binary', sample_weight=None)

#confusion matrix
cm = metrics.confusion_matrix(y_test, model.predict(X_test))
print "Confusion matrix: \n"
print "-Legend"
print np.array([['True "not disaster"', 'False "disaster"'],['False "not disaster"', 'True "disaster"']])
print "\n-Prediction"
print cm

print "\n-Precision"
print cm[1][1]/ ((cm[1][1] + cm[0][1])*1.0)

print "\n-Recall"
print cm[1][1]/ ((cm[1][0]+cm[1][1])*1.0)
print "\n"