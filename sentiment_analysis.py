#Alec Larsen - University of the Witwatersrand, South Africa, 2012 import shlex, subprocess

import shlex
import subprocess
import sys
import os
import csv

# tweet_category_file = "./output/tweet.category.csv"
tweet_category_file = "./data/output/20160903.txt"

tweet_senti_file = "./output/tweets_senti.csv"


def SentiStrength(tweet):
    #open a subprocess using shlex to get the command line string into the correct args list format
    p = subprocess.Popen(shlex.split("java -jar SentiStrength.jar stdin sentidata data/SentStrength_Data/ trinary"),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
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
    moods=[]
    mood_stats = {}  # counting frequency of tweet
    with open(tweet_input,"r") as tweetfile:
        rd=csv.reader(tweetfile, delimiter=delimiter)
        reader=[]   # list of tweets
        for item in rd:
            reader.append(item)
    
        for row in reader:
            res=SentiStrength(row[tweet_index])
            # print res
            mood = int(res.split()[2])
            moods.append(mood)
            if mood_stats.has_key(mood):
                mood_stats[mood] = mood_stats[mood] + 1
            else:
                mood_stats[mood] = 1

    print mood_stats

    with open(tweet_input, "r") as f:
        with open(tweet_output, "wb") as f2:
            rd=csv.reader(f)
            wr=csv.writer(f2)
            i=0

            for row in rd:
                wr.writerow(row+[moods[i]])
                i+=1

if __name__=="__main__":
    sensiment_analyzer(tweet_category_file, tweet_senti_file, '\t', 6)
