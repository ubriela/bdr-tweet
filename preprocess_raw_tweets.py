
"""
extract raw tweet and output "clean" tweets and a dictionary of words
"""

import csv
import re

input_filename = "./data/CL_raw_training.csv"

output_filename = "./data/CL_refined_training.csv"
vocab_filename = "./data/Tweets.vocab"

def read_data(filename):
    data1=[]
    data2=[]
    file_in1=open(filename,"r")
    datareader=csv.reader(file_in1)

    for line in datareader:
        row=line[1]
        row=re.sub(r"RT @\S+", "",row)
        row=re.sub(r"MT @\S+", "",row)
        row=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",row).split()) #remove hyperlinks 
        row=row.lower()
        data1.append([line[0],row])
        row=row.split()
        data2.append(row)
    return data2,data1
    
def save_data(save_tweets,output_filename):
    f_out=open(output_filename,"w")

    wr = csv.writer(f_out,lineterminator='\n')
    wr.writerows(save_tweets)
    f_out.close()
    return

"""
make vocabulary from refined tweets
"""
def make_vocab(refined_tweets,vocab_filename):
    vocab=set()
    
    for tweet in refined_tweets:
        for word in tweet:
            vocab.add(word)
    
    vocab=sorted(list(vocab))
    f_out=open(vocab_filename,"w")
    for word in vocab:
        f_out.write(word+"\n")
    return
    
def main():
    global input_filename,output_filename,vocab_filename
    refined_tweets,save_tweets=read_data(input_filename)
    save_data(save_tweets,output_filename)
    make_vocab(refined_tweets,vocab_filename)
    print "Created refined traning data and vocabulary file"
    
main()
