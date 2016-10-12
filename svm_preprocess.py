"""
process train and test data to output two files in SVM format

"""

import csv
import sys
import random
import re
from tweet_tokenizer import tokenize


"""
read vocab file and output a dictionary <word, word_index (i.e., line_number)>
"""
def get_vocab(vocab_file):
    c=[]
    vocab={}
    input_file=open(vocab_file,"r")
    for line in input_file:
        c.append(line.replace("\n",""))
    for i in xrange(0,len(c)):
        vocab[c[i]]=i+1
    input_file.close()
    return vocab

"""
for each tweet, return a list of distict words and their frequencies
"""
def read_train_data(filename, vocab, labels_map, train_text_index, train_label_index, delimiter="\t"):
    
    file_in1=open(filename,"r")
    datareader=csv.reader(file_in1, delimiter=delimiter)
    tokens=[] #
    
    for line in datareader:
        label = line[train_label_index]
        if label not in labels_map:
            print 'label does not exist', label
            continue
        tempList = [str(labels_map[label])]
        tempDict={} # <word_index, number of times the word appear in tweet>
        x=tokenize(line[train_text_index])
        # for each word in tweet (x)
        for item in x:
            if len(item)>0 and len(item.strip('\'"?,.')) > 0:
                if vocab[item] in tempDict.keys():
                    tempDict[vocab[item]]+=1
                else:
                    tempDict[vocab[item]]=1

        y=list(tempDict.keys())
        y.sort() # sorted word_indices
        for key in y:
                a=str(str(key)+":"+str(tempDict[key]))

                tempList.append(a)
        b=" ".join(tempList)    #  a concatnated string of a list of " sorted_word_index:appear_time"
        #print tokens
        tokens.append(b)

    return tokens


"""
Similar to read_Training_Tweets (for each tweet, return a list of distict words and their frequencies)
but this function read test data and all tweets are informative
"""
def read_test_data(filename, vocab, labels_map, test_text_index, test_label_index, delimiter='\t'):
    
    complete=[]
    for n in [filename]:
        
        y=open(n,"r")
        datareader=csv.reader(y, delimiter=delimiter)
        tokens=[]
        
        for line in datareader:
            if line==[]:
                continue
            else:
                label = line[test_label_index]
                if label not in labels_map:
                    print 'label does not exist', label
                    continue
                tempList = [str(labels_map[label])]
                tempDict={}
                # row=line[test_text_index]#.replace("\n"," ")
                # row=re.sub(r"RT @\S+", "",row)
                # row=re.sub(r"MT @\S+", "",row)
                # row=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",row).split())
                # x=row.lower().split()   # array of words in tweet
                x = tokenize(line[test_text_index])
            if len(x)<1 or x==" ":
                continue
            # print x
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
def save_data(train_data,test_data,train_file,test_file):

    output_file=open(train_file,"w")
    for line in train_data:
       output_file.write(line+"\n")
    output_file.close()

    output_file2=open(test_file,"w")
    for line2 in test_data:
       output_file2.write(line2+"\n")
    output_file2.close()