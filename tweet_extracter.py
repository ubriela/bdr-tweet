from twython import Twython
import csv

def main():
    TWITTER_APP_KEY = 'VIlDdi6LKAjGJxUhsxZNc1P1t' #supply the appropriate value
    TWITTER_APP_KEY_SECRET = 'oh6dwllSvDszpxp100hZWs9jLrNnRzFw8ixgtIlzOlrjOGjfG5' 
    TWITTER_ACCESS_TOKEN = '573560865-y1IBXNelm6YbmMeS4E6vSbbOgng7cSlNIGfLp1sW'
    TWITTER_ACCESS_TOKEN_SECRET = 'Snw836BTOUDVy56Tg6o3IVtjkZwyUUtfosIhzNEwnHRSx'
    
    t = Twython(app_key=TWITTER_APP_KEY, app_secret=TWITTER_APP_KEY_SECRET, oauth_token=TWITTER_ACCESS_TOKEN, oauth_token_secret=TWITTER_ACCESS_TOKEN_SECRET)
    
    with open('./arg_file.csv') as argfile:
        rd=csv.reader(argfile)
        reader=[]
        for item in rd:
            reader.append(item)
        #print(reader)
        hashtags=reader[0]
        userhandle=reader[3]
        counth=reader[1]
        countu=reader[4]
        
        i=0
        for item in hashtags[1:]:
            if item!='':
                #print(item)
                i+=1
                cnt=counth[i]
                rows=get_tweets(t, item, cnt)
                try:
                    with open('./data/tweets_hashtag.csv', 'ab') as file3:
                        wr=csv.writer(file3)
                        wr.writerows(rows)
                        
                except:
                    pass
            
        i=0
        for item in userhandle[1:]:
            if item!='':
                i+=1
                cnt=countu[i]
                rows=get_tweets(t, item, cnt)
                
                try:
                    with open('./data/tweets_users.csv', 'ab') as file3:
                        wr=csv.writer(file3)
                        wr.writerows(rows)
                        
                except:
                    pass
            
def get_tweets(t, q, cnt):        
                
        #print(data)
    
    search = t.search(q=q, cnt=cnt, lang='en')
    
    tweets = search['statuses']
    
    rows=[]
    missed=0
    i=0
    for tweet in tweets:
        try:
            id=text=retweet=retweetc=geo=time=''
            row=[]
            i+=1
            #print(i)
            #print('tweet: '+str(tweet))
            #print("\n")
            #print('id: '+tweet['id_str']+ '\n'+ 'text: '+tweet['text']+'\n'+ 'retweet: '+str(tweet['retweeted'])+'\n'+ 'retweet_count: '+str(tweet['retweet_count'])+'\n'+ 'geo: '+str(tweet['geo'])+'\n'+ 'time: '+tweet['created_at']+'\n'+'screenname: '+str(tweet['entities']['user_mentions'])+'\n\n\n')
            id=str(tweet['id_str'])
            time=str(tweet['created_at'])
            text=str(tweet['text'])
            text.replace('(', '')
            text.replace(')', '')
            text.replace('"', '')
            text.replace("'", '')
            text.replace('\\', '')
            if tweet['geo']:
                geo=str(tweet['geo'])
            retweet=str(tweet['retweeted'])
            retweetc=str(tweet['retweet_count'])
            #row.append(str(tweet['id_str'])).append(str(tweet['text'])).append(str(tweet['retweeted'])).append(str(tweet['retweet_count']))
            rows.append((q,id, time, text, geo, retweet, retweetc))
        except:
            missed+=1
    
    return rows    
    #try:
        #with open('tweets_ae.csv', 'wb') as file3:
            #wr=csv.writer(file3)
            #wr.writerows(rows)
                
    #except:
        #pass

if __name__ == '__main__':
    main()