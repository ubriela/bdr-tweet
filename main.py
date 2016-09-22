"""

"""
import os
import platform

platform = platform.system()

# using proper library depends on OS type
if platform == 'Windows':
    svm_learn = '.\lib\svm_learn.exe'
    svm_classify = '.\lib\svm_classify.exe'
else:
    svm_learn = './lib/svm_learn'
    svm_classify = './lib/svm_classify'

os.system("python preprocess_raw_tweets.py")

print os.system("python svm_preprocess.py")
print os.system(svm_learn + " ./data/Tweet_Train.txt ./output/tweet.model")
print "Created model ./output/tweet.model"
print os.system(svm_classify + " ./data/Tweet_Test.txt ./output/tweet.model ./output/svm_output.txt")
print "Output classifier result ./output/svm_output.txt"
print os.system("python svm_postprocess.py")

print os.system("python categorization.py")

print os.system("python sentiment_analysis.py")

print ("Finished")