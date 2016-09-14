"""
categorize tweets into categories, e.g., food, water, etc.
append at the end of each tweet
"""
from stemming.porter2 import stem
import csv
from PyDictionary import PyDictionary
dictionary=PyDictionary()

informative_tweet = "./output/informative_tweet.csv"
test_delimiter, test_text_index = ",", 3

tweet_category_file = "./output/tweet.category.csv"

def main():

    tweets=[]
    newDataset=[]
    with open(informative_tweet, 'rU') as f:
        datareader=csv.reader(f, delimiter=test_delimiter)
        for each in datareader:
            tweets.append(each)

    categories = ['Food', 'Water', 'Shelter', 'Medicine']
    weight=0.2
        
    dictionary={'Food':[], 'Water':[], 'Shelter':[], 'Medicine':[]}    
        
            
        
    """
    Extracting the tweets from csv
    """
    #Food
    with open('./data/Food.csv', 'rU') as f:
        for each in f:
            dictionary['Food'].append(each)
    #Water
    with open('./data/Water.csv', 'rU') as f:
        for each in f:
            dictionary['Water'].append(each)
    #Shelter
    with open('./data/Shelter.csv', 'rU') as f:
        for each in f:
            dictionary['Shelter'].append(each)
    #Medicine
    with open('./data/Medicine.csv', 'rU') as f:
        for each in f:
            dictionary['Medicine'].append(each)

    for tweet in tweets:
        inputString = tweet[test_text_index]

        weightDict={} # {category : weight}
        for category in categories:
            weightCount=0.0
            synList = dictionary[category]
            
            if(category.lower() in inputString.lower()):
                weightCount+=weight                        
                
            for each in synList:
                a=each.lower()
                if a[:-1] in inputString.lower():
                    weightCount+=weight
            
            for each in synList:
                a=each.lower()
                if stem(a[:-1]) in inputString.lower():
                    weightCount+=weight
                    
            weightDict[category]=weightCount        
                
        maxCount = max(weightDict.values())

        if(weightDict.values().count(maxCount)==1): # one group
            for key in weightDict.keys():
                if(weightDict[key]==maxCount):
                    tweet.append(key)   # category is the group with maximum weight
        elif(maxCount==0.0):    # no group
            tweet.append('Unknown')
        else: # multiple groups
            temp=[]
            for key in weightDict.keys():
                if(weightDict[key]==maxCount):
                    temp.append(key)

            tempString = ",".join(temp)
            tweet.append(tempString)

        newDataset.append(tweet)
    
    with open(tweet_category_file, "wb") as csvfile:
        areawriter = csv.writer(csvfile, delimiter=',')
        for l in newDataset:
            areawriter.writerow(l)

    print "Categorized tweets into groups, e.g., food, water, etc: " + tweet_category_file

main()
