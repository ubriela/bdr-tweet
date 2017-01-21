
# this code genrates the tweet sentiments
import shlex
import subprocess
import io
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import csv
'''
import resource

resource.setrlimit(
    resource.RLIMIT_CORE,
    (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
print "Current RLIMIT_NOFILE limit:", soft, hard, "Changing to 3000..."
resource.setrlimit(resource.RLIMIT_NOFILE, (3000, hard))
'''
"""
    run senstiment analysis for a file, including a set of tweets
    each line of input file is a tweet's information
    tweet_index is the index of the text in each line
    """

def SentiStrength(tweet):
    #open a subprocess using shlex to get the command line string into the correct args list format
    p = subprocess.Popen(shlex.split("java -jar SentiStrength.jar stdin sentidata data/SentStrength_Data/ binary"),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    #communicate via stdin the string to be rated. Note that all spaces are replaced with +
    try:

        stdout_text, stderr_text = p.communicate(tweet.replace(" ", "+").encode())
        #print stdout_text, stderr_text
    except UnicodeDecodeError:
        return "false"
    #remove the tab spacing between the positive and negative ratings. e.g. 1    -5 -> 1-5
    stdout_text = stdout_text.rstrip().decode().replace("\t","")
    return stdout_text

def sensiment_analyzer(tweet_input, delimiter='\t', tweet_index=2):
    qw = 0
    count = 0
    neg = 0
    tweet = []
    mood_stats = []  # counting frequency of tweet
    with io.open(tweet_input, 'rU', encoding='utf-8') as f:
        for line in f:
            #print line
            res = SentiStrength((line))
            #print res
            res = [x.strip() for x in res.split(" ")]
            #print res[-1]

            if int(res[-1]) == 1:
                neg += 1
            count += 1



                #mood_stats.append(int(res[-1]))
                #tweet.append(a)
                #f2.write('\t'.join(a) + '\t' + str(mood) + '\n')

            qw += 1
            if qw % 20 == 0:
                print 'Processed tweets: ' + str(qw)

        print neg, count





sensiment_analyzer("./model/word2vec-sentiments-master/train_test/test-pos.txt")
#sensiment_analyzer("./data/austin/demo.txt", "./data/austin/demo1.txt")