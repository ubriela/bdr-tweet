"""

"""
import os

os.system("python preprocess_rawfile.py")
print
os.system("python svm_preprocess.py")
print
os.system("svm_learn.exe ./data/Tweet_Train.txt ./output/tweet.model")
print
"Created model ./output/tweet.model"
print
os.system("svm_classify.exe ./data/Tweet_Test.txt ./output/tweet.model ./output/svm_output.txt")
print
"Output classifier result ./output/svm_output.txt"
print
os.system("python svm_postprocess.py")
print 
os.system("python categorization.py")
print
os.system("python sentiment_analysis.py")

print ("Finished")