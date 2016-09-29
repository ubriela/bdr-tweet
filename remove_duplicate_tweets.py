import difflib

file_path = "./data/test_data.csv"

with open(file_path) as f:
    tweets = [l.lower() for l in f.readlines()]
    for i in range(len(tweets)):
        for j in range(i+1,len(tweets)):
            if difflib.SequenceMatcher(None, tweets[i], tweets[j]).ratio() > 0.9:
                print i, j
                print tweets[i]
                print tweets[j]
