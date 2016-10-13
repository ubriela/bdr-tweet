"""
Create datasets from CrisisLex datasets
"""
import numpy as np
import collections
import glob
import csv
import re

CrisisLexT26Folder = "./data/CrisisLex/data/CrisisLexT26"
CrisisLexT6Folder = "./data/CrisisLex/data/CrisisLexT6"
CL_data = "./data/CrisisLex/CrisisLex27K.csv"

def clean_line(row):
    row = re.sub(r"RT @\S+", "", row)
    row = re.sub(r"MT @\S+", "", row)
    row = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", row).split())  # remove hyperlinks
    row = row.lower()
    row.replace('\t', ' ')
    return row

# data = np.loadtxt(CrisisLexT6Folder + "/2012_Sandy_Hurricane/2012_Sandy_Hurricane-ontopic_offtopic.csv", dtype='str', delimiter=',', skiprows = 1)
if False:
    with open(CrisisLexT6Folder + "/2012_Sandy_Hurricane/2012_Sandy_Hurricane-ontopic_offtopic.csv") as f:
        on_topic = open(CrisisLexT6Folder + "/2012_Sandy_Hurricane/on-topic.txt", "w")
        off_topic = open(CrisisLexT6Folder + "/2012_Sandy_Hurricane/off-topic.txt", "w")
        for line in f.readlines()[1:]:
            vals = line.strip().split(',')
            if len(vals) == 3:
                if vals[2] == 'on-topic':
                    on_topic.write(vals[1].strip('\"') + "\n")
                elif vals[2] == 'off-topic':
                    off_topic.write(vals[1].strip('\"') + "\n")
            else:
                length = len(vals)
                # print length, line

        on_topic.close()
        off_topic.close()

for file in glob.glob(CrisisLexT26Folder + "/*/*labeled.csv"):
    with open(file) as f:
        output_name = file.split('\\')[len(file.split('\\'))-2]
        print output_name
        output = open(CrisisLexT26Folder + '/' + output_name + '.txt', "w")
        for line in f.readlines()[1:]:
            vals = line.strip().split(',')
            if len(vals) == 5:
                output.write(vals[1].strip('\"') + "\n")
            elif len(vals) > 5:
                length = len(vals)
                tweet = re.sub(r"\s+", " ", ','.join(vals[1:length - 3])).strip('\"')
                output.write(tweet + "\n")

        output.close()

if False:
    all_labeled_data = []
    for file in glob.glob(CrisisLexT26Folder + "/*/*labeled.csv"):
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

# np.savetxt(CL_data, all_labeled_data, fmt='%s', delimiter='\t')