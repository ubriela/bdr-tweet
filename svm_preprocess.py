"""
process train and test data to output two files in SVM format

"""

import csv
import sys
import random
import re

input_train_file="./data/CL_refined_training.csv"
input_test_file = "./data/tweets_hashtag.csv" # "./data/output/test.txt" #
test_delimiter, test_text_index = ",", 3

train_file = "./data/Tweet_Train.txt"
test_file = "./data/Tweet_Test.txt"

"""
read vocab file and output a dictionary <word, word_index (i.e., line_number)>
"""
def get_vocab():
    c=[]
    vocab={}
    input_file=open("./data/Tweets.vocab","r")
    for line in input_file:
        c.append(line.replace("\n",""))
    for i in xrange(0,len(c)):
        vocab[c[i]]=i+1
    input_file.close()
    return vocab


"""
for each tweet, return a list of distict words and their frequencies
"""
def read_Training_Tweets(filename,vocab):  
    
    file_in1=open(filename,"r")
    datareader=csv.reader(file_in1)
    tokens=[] #
    
    for line in datareader:
        if line[0]=="Informative":
            tempList=['1']
        else:
            tempList=['-1']
        
        tempDict={} # <word_index, number of times the word appear in tweet
        x=line[1].strip().replace("\n","").split()

        # for each word in tweet (x)
        for item in x:
            if len(item)>0:
                # if
                if vocab[item.strip()] in tempDict.keys():
                    tempDict[vocab[item]]+=1
                else:
                    tempDict[vocab[item]]=1

        y=list(tempDict.keys())
        y.sort() # sorted word_indices
        for key in y:
                a=str(str(key)+":"+str(tempDict[key]))

                tempList.append(a)
        b=" ".join(tempList)    #  a concatnated string of a list of " sorted_word_index:appear_time"

        tokens.append(b)

    return tokens


"""
Similar to read_Training_Tweets (for each tweet, return a list of distict words and their frequencies)
but this function read test data and all tweets are informative
"""
def read_Test_Tweets(filename,vocab):
    
    complete=[]
    for n in [filename] :
        
        y=open(n,"r")
        datareader=csv.reader(y, delimiter=test_delimiter)
        tokens=[]
        
        for line in datareader:
            if line==[]:
                continue
            else:
                # tempList=[line[0]]
                tempList = ['1']
                tempDict={}
                row=line[test_text_index].replace("\n","")
                row=re.sub(r"RT @\S+", "",row)
                row=re.sub(r"MT @\S+", "",row)
                row=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",row).split())
                x=row.lower().split()   # array of words in tweet
            if len(x)<1 or x==" ":
                continue
            for item in x:
                if len(item)>0:
                    if item.strip() in vocab.keys(): # discard word that is not in vocab
                        if vocab[item.strip()] in tempDict.keys():
                            tempDict[vocab[item]]+=1
                        else:
                            tempDict[vocab[item]]=1

            y=list(tempDict.keys())
            y.sort()
            for key in y:
                a=str(str(key)+":"+str(tempDict[key]))
                tempList.append(a)
            b=" ".join(tempList)

            tokens.append(b)
        
        complete.extend(tokens)
    return complete

"""
output train and test data into two files
"""
def save_data(train_data,test_data):

    output_file=open(train_file,"w")
    for line in train_data:
       output_file.write(line+"\n")
    output_file.close()

    output_file2=open(test_file,"w")
    for line2 in test_data:
       output_file2.write(line2+"\n")
    output_file2.close()

def main():
    global input_train_file,input_test_file
    Tweet_vocab=get_vocab()
    train_Tweets=read_Training_Tweets(input_train_file,Tweet_vocab)
    test_Tweets=read_Test_Tweets(input_test_file,Tweet_vocab)
    
    save_data(train_Tweets,test_Tweets)
    print ("Prerocess train and test data to output two corresponding files in SVM format: " + train_file + "\t" + test_file)
    
main()