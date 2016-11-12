'''
Gets text content for tweet IDs
http://stackoverflow.com/questions/28384588/twitter-api-get-tweets-with-specifc-id
'''

# standard
from __future__ import print_function
import getopt
import logging
import os
import sys
import glob
import re
import time
# import traceback
# third-party: `pip install tweepy`
import tweepy

# global logger level is configured in main()
Logger = None

TWEET_PATH = "state_id_2014-08-25/*"

# Generate your own at https://apps.twitter.com/app
CONSUMER_KEY = 'VIlDdi6LKAjGJxUhsxZNc1P1t'
CONSUMER_SECRET = 'oh6dwllSvDszpxp100hZWs9jLrNnRzFw8ixgtIlzOlrjOGjfG5'
OAUTH_TOKEN = '573560865-y1IBXNelm6YbmMeS4E6vSbbOgng7cSlNIGfLp1sW'
OAUTH_TOKEN_SECRET = 'Snw836BTOUDVy56Tg6o3IVtjkZwyUUtfosIhzNEwnHRSx'

def get_tweet_id(line):
    '''
    Extracts and returns tweet ID from a line in the input.
    '''
    # (tagid,_timestamp,_sandyflag) = line.split('\t')
    # (_tag, _search, tweet_id) = tagid.split(':')
    # return tweet_id
    return line.strip()

def get_tweets_single(twapi, idfilepath):
    '''
    Fetches content for tweet IDs in a file one at a time,
    which means a ton of HTTPS requests, so NOT recommended.

    `twapi`: Initialized, authorized API object from Tweepy
    `idfilepath`: Path to file containing IDs
    '''
    # process IDs from the file
    with open(idfilepath, 'rb') as idfile:
        for line in idfile:
            tweet_id = get_tweet_id(line)
            Logger.debug('Fetching tweet for ID %s', tweet_id)
            try:
                tweet = twapi.get_status(tweet_id)
                print('%s,%s' % (tweet_id, tweet.text.encode('UTF-8')))
            except tweepy.TweepError as te:
                Logger.warn('Failed to get tweet ID %s: %s', tweet_id, te.message)
                # traceback.print_exc(file=sys.stderr)
        # for
    # with

def get_tweet_list(twapi, idlist, file_out):
    '''
    Invokes bulk lookup method.
    Raises an exception if rate limit is exceeded.
    '''
    # fetch as little metadata as possible
    while True:
        try:
            tweets = twapi.statuses_lookup(id_=idlist, include_entities=False, trim_user=True)
            for tweet in tweets:
                # "tweet content","date time","user id",lat,lon
                if tweet.geo is not None:
                    content = re.sub("\s\s+", " ", tweet.text.encode('UTF-8'))
                    content = content.replace("\n", " ")
                    line = ','.join(map(str, [content, tweet.created_at, tweet.user.id, tweet.geo['coordinates'][0], tweet.geo['coordinates'][1]])) + '\n'
                    file_out.write(line)

        except tweepy.TweepError, e:
            time.sleep(60 * 15)
            print ("TweepError raised, ignoring and continuing.")
            print (e)
            continue
        except StopIteration:
            break
        break

def get_tweets_bulk(twapi, idfilepath):
    '''
    Fetches content for tweet IDs in a file using bulk request method,
    which vastly reduces number of HTTPS requests compared to above;
    however, it does not warn about IDs that yield no tweet.

    `twapi`: Initialized, authorized API object from Tweepy
    `idfilepath`: Path to file containing IDs
    '''
    # process IDs from the file
    tweet_ids = list()
    parts = idfilepath.split('.')
    filepath = parts[0][:-3] + '.txt'
    file_out = open(filepath, 'w')
    with open(idfilepath, 'rb') as idfile:
        for line in idfile:
            tweet_id = get_tweet_id(line)
            Logger.debug('Fetching tweet for ID %s', tweet_id)
            # API limits batch size to 100
            if len(tweet_ids) < 100:
                tweet_ids.append(tweet_id)
            else:
                get_tweet_list(twapi, tweet_ids, file_out)
                tweet_ids = list()
    # process rump of file
    if len(tweet_ids) > 0:
        get_tweet_list(twapi, tweet_ids, file_out)
    file_out.close()

def usage():
    print('Usage: get_tweets_by_id.py [options] folder/file')
    print('    -s (single) makes one HTTPS request per tweet ID')
    print('    -v (verbose) enables detailed logging')
    sys.exit()

def main(args):
    logging.basicConfig(level=logging.WARN)
    global Logger
    Logger = logging.getLogger('get_tweets_by_id')
    bulk = True
    try:
        opts, args = getopt.getopt(args, 'sv')
    except getopt.GetoptError:
        usage()
    for opt, _optarg in opts:
        if opt in ('-s'):
            bulk = False
        elif opt in ('-v'):
            Logger.setLevel(logging.DEBUG)
            Logger.debug("verbose mode on")
        else:
            usage()
    if len(args) != 1:
        usage()
    idfile = args[0]
    if not os.path.isfile(idfile):
        for file in glob.glob(TWEET_PATH):
            print ("parsing " +  str(file))
            parse_one_file(file, bulk)
    else:   # this is a file
        parse_one_file(idfile, bulk)

def parse_one_file(idfile, bulk):
    # connect to twitter
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    api = tweepy.API(auth)

    # hydrate tweet IDs
    if bulk:
        get_tweets_bulk(api, idfile)
    else:
        get_tweets_single(api, idfile)

if __name__ == '__main__':
    main(sys.argv[1:])