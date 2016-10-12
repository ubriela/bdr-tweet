"""
extract raw tweet and output "clean" tweets and a dictionary of words
"""

import csv
from tweet_tokenizer import tokenize

def read_data(filename,tweet_index):
    all_rows=[]
    all_tokens=[]
    file_in1=open(filename,"r")
    datareader=csv.reader(file_in1,delimiter='\t')
    # next(datareader)
    for line in datareader:
        tweet=line[tweet_index]
        tokens = tokenize(tweet)
        tokenized_tweet = ' '.join(tokens)
        tokenized_row = line[0:tweet_index]
        tokenized_row.append(tokenized_tweet)
        all_rows.append(tokenized_row)
        all_tokens.append(tokens)
    return all_tokens,all_rows
    
def save_vocab_tweets(save_tweets,output_filename):
    f_out=open(output_filename,"w")

    wr = csv.writer(f_out,lineterminator='\n',delimiter='\t')
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