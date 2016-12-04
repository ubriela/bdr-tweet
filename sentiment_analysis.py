#Alec Larsen - University of the Witwatersrand, South Africa, 2012 import shlex, subprocess

import shlex
import subprocess
import sys
import os
import csv
import re
import numpy as np
from sklearn.metrics import precision_recall_fscore_support as pr

#tweet_category_file = "./output/tweet.category.csv"
# tweet_category_file = "./data/election_neg.txt"
tweet_category_file = "./data/sentiment140/testdata.manual.2009.06.14.csv"

tweet_senti_file = "./data/sentiment140/testdata.manual.2009.06.14_output.csv"

tweet_index = 5 #6


def SentiStrength(tweet):
    #open a subprocess using shlex to get the command line string into the correct args list format
    p = subprocess.Popen(shlex.split("java -jar SentiStrength.jar stdin sentidata data/SentStrength_Data/ binary"),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    #communicate via stdin the string to be rated. Note that all spaces are replaced with +
    stdout_text, stderr_text = p.communicate(tweet.replace(" ", "+").encode())
    #remove the tab spacing between the positive and negative ratings. e.g. 1    -5 -> 1-5
    stdout_text = stdout_text.rstrip().decode().replace("\t","")
    return stdout_text


"""
run senstiment analysis for a file, including a set of tweets
each line of input file is a tweet's information
tweet_index is the index of the text in each line
"""
def sensiment_analyzer(tweet_input, tweet_output, delimiter=',', tweet_index=3):
    true_moods = []
    estimated_moods = []  # counting frequency of tweet
    mood_mapping = {0:-1, 4:1}
    with open(tweet_input,"r") as tweetfile:
        rd=csv.reader(tweetfile)
    
        for row in rd:
            try:
                s = unicode()
            except UnicodeDecodeError:
                s = str(s).encode('string_escape')
                s = unicode(s)
            s = row[tweet_index]
            if not mood_mapping.has_key(int(row[0])):
                continue
            res=SentiStrength(s)
            mood = int(res.split()[2])
            estimated_moods.append(mood)
            true_mood = mood_mapping[int(row[0])]

            true_moods.append(true_mood)

            print true_mood, '\t', mood

    bPrecis, bRecall, bFscore, bSupport = pr(true_moods, estimated_moods, average='macro', labels=[-1,1])
    print bPrecis, bRecall, bFscore, bSupport


    # with open(tweet_input, "r") as f:
    #     with open(tweet_output, "wb") as f2:
    #         rd=csv.reader(f)
    #         wr=csv.writer(f2)
    #         i=0
    #
    #         for row in rd:
    #             wr.writerow(row+[estimated_moods[i]])
    #             i+=1

# These are for regularizing HTML entities to Unicode:
html_entity_digit_re = re.compile(r"&#\d+;")
html_entity_alpha_re = re.compile(r"&\w+;")
amp = "&amp;"

def html2unicode(s):
    """
    Internal method that seeks to replace all the HTML entities in
    s with their corresponding unicode characters.
    """
    # First the digits:
    ents = set(html_entity_digit_re.findall(s))
    if len(ents) > 0:
        for ent in ents:
            entnum = ent[2:-1]
            try:
                entnum = int(entnum)
                s = s.replace(ent, unichr(entnum))
            except:
                pass
    # Now the alpha versions:
    ents = set(html_entity_alpha_re.findall(s))
    ents = filter((lambda x: x != amp), ents)
    for ent in ents:
        entname = ent[1:-1]
        try:
            s = s.replace(ent, unichr(htmlentitydefs.name2codepoint[entname]))
        except:
            pass
        s = s.replace(amp, " and ")
    return s

def split_datasets(tweet_input, tweet_index=3):
    mood_mapping = {0: -1, 2: 0, 4: 1}
    with open(tweet_input, "r") as tweetfile:
        rd = csv.reader(tweetfile)
        train_neg = []
        train_neu = []
        train_pos = []
        for row in rd:
            s = None
            try:
                s = unicode(s)
            except UnicodeDecodeError:
                s = str(s).encode('string_escape')
                s = unicode(s)

            # Fix HTML character entitites:
            s = html2unicode(s)

            s = row[tweet_index]
            true_mood = mood_mapping[int(row[0])]
            if true_mood == -1:
                train_neg.append(s)
            elif true_mood == 0:
                train_neu.append(s)
            elif true_mood == 1:
                train_pos.append(s)

        np.savetxt('./test/word2vec-sentiments-master/train-neg.txt', train_neg, fmt='%s')
        # np.savetxt('./test/word2vec-sentiments-master/train_neu.txt', train_neu, fmt='%s')
        np.savetxt('./test/word2vec-sentiments-master/train-pos.txt', train_pos, fmt='%s')

if __name__=="__main__":
    sensiment_analyzer(tweet_category_file, tweet_senti_file, '\t', tweet_index)
    # split_datasets(tweet_category_file, tweet_index)
