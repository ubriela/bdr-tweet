import difflib

file_path = "./data/test_data.csv"

with open(file_path) as f:
    tweets = [l.lower() for l in f.readlines()]
    for i in range(len(tweets)):
        duplicate = False
        for j in range(0,i):
            if difflib.SequenceMatcher(None, tweets[i], tweets[j]).ratio() > 0.9:
                duplicate = True
                continue
        if duplicate == False:
            print tweets[i].strip()
