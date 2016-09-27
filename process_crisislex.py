"""
Create a training dataset from CrisisLex datasets
"""
import numpy as np
import collections
import glob
import csv
import re

CrisisLexFolder = "./data/CrisisLex/data/CrisisLexT26"
CL_training = "./data/CL_training.csv"

def clean_line(row):
    row = re.sub(r"RT @\S+", "", row)
    row = re.sub(r"MT @\S+", "", row)
    row = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", row).split())  # remove hyperlinks
    row = row.lower()
    row.replace('\t', ' ')
    return row


all_labeled_data = []
for file in glob.glob(CrisisLexFolder + "/*/*labeled.csv"):
    with open(file) as f:
        for line in f.readlines()[1:]:
            vals = line.strip().split(',')
            if len(vals) == 5:
                all_labeled_data.append('\t'.join([vals[0].strip('\"'), vals[2].strip(),vals[3],vals[4], re.sub(r"\s+", " ", vals[1].strip('\"'))]))
            elif len(vals) > 5:
                length = len(vals)
                all_labeled_data.append('\t'.join([vals[0].strip('\"'), vals[length-3], vals[length-2], vals[length-1], re.sub(r"\s+", " ", ','.join(vals[1:length-3]))]))

print 'Number of training tweets:', len(all_labeled_data)

# for line in all_labeled_data:
#     print line

np.savetxt(CL_training, all_labeled_data, fmt='%s', delimiter='\t')