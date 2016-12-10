import csv
#from word2vec_sentifier import train, predict
#classifier = train()
import shlex
import subprocess

import csv



"""
    run senstiment analysis for a file, including a set of tweets
    each line of input file is a tweet's information
    tweet_index is the index of the text in each line
    """

def SentiStrength(tweet):
    #open a subprocess using shlex to get the command line string into the correct args list format
    p = subprocess.Popen(shlex.split("java -jar SentiStrength.jar stdin sentidata data/SentStrength_Data/ binary"),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    #communicate via stdin the string to be rated. Note that all spaces are replaced with +
    stdout_text, stderr_text = p.communicate(tweet.replace(" ", "+").encode())
    #remove the tab spacing between the positive and negative ratings. e.g. 1    -5 -> 1-5
    stdout_text = stdout_text.rstrip().decode().replace("\t","")
    return stdout_text

def sensiment_analyzer(neg_ratio, tweet_input, tweet_output, delimiter=',', tweet_index=0):
    qw = 0
    count_pos = 0
    count_neg = 0
    mood_stats = {}  # counting frequency of tweet
    with open(tweet_input, 'rU') as f:
        with open(tweet_output, "wb") as f2:
            rd = csv.reader(f, delimiter=delimiter)
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

                res=SentiStrength(a[tweet_index])
                #sentiment = predict(classifier, [a[tweet_index]])
                mood = int(res[0])
                if mood == -1:
                    count_neg += 1
                elif mood == 1:
                    count_pos += 1

                a.append(str(mood))
                # print a
                f2.write(', '.join(a) + '\n')
                qw += 1
                if qw % 20 == 0:
                    print 'Processed tweets: ' + str(qw)

    print "neg =", count_neg
    print "pos = ", count_pos
    print (count_neg / ((count_pos + count_neg) * 1.0))
    print (count_neg / (qw * 1.0))

    return neg_ratio.append(count_neg / ((count_pos + count_neg) * 1.0))