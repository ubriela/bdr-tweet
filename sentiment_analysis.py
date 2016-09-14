#Alec Larsen - University of the Witwatersrand, South Africa, 2012 import shlex, subprocess

import shlex
import subprocess
import sys
import os
import csv

tweet_category_file = "./output/tweet.category.csv"
tweet_senti_file = "./output/tweets_senti.csv"

def RateSentiment(sentiString):
    #open a subprocess using shlex to get the command line string into the correct args list format
    p = subprocess.Popen(shlex.split("java -jar SentiStrength.jar stdin sentidata data/SentStrength_Data/ binary"),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    #communicate via stdin the string to be rated. Note that all spaces are replaced with +
    stdout_text, stderr_text = p.communicate(sentiString.replace(" ","+").encode())
    #remove the tab spacing between the positive and negative ratings. e.g. 1    -5 -> 1-5
    stdout_text = stdout_text.rstrip().decode().replace("\t","")
    return stdout_text


def main():
    tweets=[]
    #with open("result.txt", "w") as f:
    results=[]
    with open(tweet_category_file,"r") as tweetfile:
        rd=csv.reader(tweetfile)
        reader=[]   # list of tweets
        for item in rd:
            reader.append(item)
    
        for row in reader:
            res=RateSentiment(row[3])
            part=res.split(' ')
            results.append(part[2])
            
    #print(results)
    with open(tweet_category_file, "r") as f:
        with open(tweet_senti_file, "wb") as f2:
            rd=csv.reader(f)
            wr=csv.writer(f2)
            i=0

            for row in rd:
                #print((row).append("as"))
                #row.replace('\n','')
                
                wr.writerow(row+[results[i]])
                
                i+=1
        
    
    
        #for tweet in tweets:
            
    #RateSentiment("I'm working on it")

if __name__=="__main__":
    main()
