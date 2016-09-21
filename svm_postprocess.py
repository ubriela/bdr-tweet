
"""
Only output informative tweets

"""
import csv
import re

input_test_file = "./data/tweets_hashtag.csv" # "./data/output/test.txt"
output_score = "./output/svm_output.txt"

output_informative_tweet = "./output/informative_tweet.csv"

def read_Test_Tweets(test_file):
    complete=[]
    for n in [test_file] :
        y=open(n,"r")
        datareader=csv.reader(y)
        tokens=[]
        
        for line in datareader:
            
            if line==[]:
                continue
            else:
                tokens.append(line)     
        complete.extend(tokens)
    return complete

def postprocess(input_file, output_score, output_file):
    Labels=["Informative","Non-Informative"]

    a=[]    # list of score for testing tweets
    output_score_file=open(output_score)
    for line in output_score_file:
        a.append(float(line.replace('\n',"")))
    output_score_file.close()

    output_labels=[]    # list of output labels corresponding to the testing tweets
    for i in xrange(len(a)):
        
        if a[i]>0:
            b=Labels[0]
        elif a[i]<0:
            b=Labels[1]
        else:
            b="UNKNOWN"
        output_labels.append(b)
    
    tweets=read_Test_Tweets(input_file)
    
    a=[]    # list of tweet with labels
    for i in xrange(len(output_labels)):
        if output_labels[i]=="Informative":
            tweets[i].append(output_labels[i])  # append label to the end of tweet
            a.append(tweets[i])
        
    
    f_out=open(output_file,"w")
    wr = csv.writer(f_out,lineterminator='\n')
    wr.writerows(a)
    f_out.close()
    print ("Postprocess tweets to output only informative tweets: " + output_informative_tweet)

postprocess(input_test_file, output_score, output_informative_tweet)