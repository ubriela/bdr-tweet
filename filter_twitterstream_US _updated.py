import oauth2 as oauth
import urllib2 as urllib
import urllib3
import httplib
import json
import datetime
import time
import os
import sys
import ssl


consumer_key="7UvZlPPrZXUl4QVVMc6K0aTV6"
consumer_secret="eSrnLcdRhbrs4zHdGKQDZa2lJOC7fildOIKcckktpTaYSp7T06"
access_token_key="1633608188-VsB2v5qqOUb8amj4InBTryK6mwmYNifkfiSNjsx"
access_token_secret="WFQzD23giH073sEhSkN4e2WsdWsT2E9QLydak4nkIqa5d"

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "POST"
timeout = 90

http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

# Construct, sign, and open a twitter request using the hard-coded credentials above.
def twitterreq(url, method, parameters):
	req = oauth.Request.from_consumer_and_token(oauth_consumer,
	                                           token=oauth_token,
	                                           http_method=http_method,
	                                           http_url=url, 
	                                           parameters=parameters)

	req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)
	
	headers = req.to_header()
	
	if http_method == "POST":
		encoded_post_data = req.to_postdata()
	else:
		encoded_post_data = None
		url = req.to_url()
	
	#opener = urllib.OpenerDirector()
	#opener.add_handler(http_handler)
	#opener.add_handler(https_handler)
	
	#print url
	#print encoded_post_data
	#headers = {'User-Agent': 'depression_tracker/0.01'}
	#response = opener.open(url, encoded_post_data, timeout)
	response = urllib.urlopen(url, encoded_post_data, timeout)
	
	return response

def fetchsamples():
	url = "https://stream.twitter.com/1.1/statuses/filter.json"
	#url = "https://199.59.148.229/1.1/statuses/sample.json"
	parameters = {'locations': '-124.848974,24.396308,-66.885444,49.384358'}
	error_code = 0
	sleep_time = 0.0
	prev_date = ''
	while True:
		try:
			response = twitterreq(url, http_method, parameters)
			for line in response:
				cur_date = time.strftime('%Y%m%d', time.localtime())
				if cur_date != prev_date:
					if prev_date != '':
						feeds_file.close()
					feeds_file = open(cur_date + '.txt', 'a')
					prev_date = cur_date
				##feeds_file.write(line.strip() + '\n')
				
				
				obj = json.loads(line[0:-1])
				if len(obj) == 1: continue

				if obj["geo"] == None: continue
				if obj["geo"]["coordinates"] == None: continue

				if obj["lang"] == "en": continue
				
				if obj["text"] == None: continue
                                #text = obj["text"].encode('utf-8')
				
				if obj["user"] == None: continue
				if obj["user"]["id_str"] == None: continue
				
				if obj["place"] == None: continue		
				if obj["place"]["country_code"] == "US":
					feeds_file.write(line.strip()+'\n')
				#print line.strip()
				#print json.loads(line.strip())['text']
		
		except (urllib3.exceptions.TimeoutError, urllib.HTTPError), e:
			sys.stderr.write('HTTPError: {0:d}. '.format(e.code) + time.strftime('%b %d, %Y %H:%M:%S', time.localtime()) + '\n')
			sys.stderr.write(str(e.reason) + '\n')
			if e.code == 420:
				if e.code == error_code:
					sleep_time = min(sleep_time*2)
				else:
					sleep_time = 60
			else:
				if e.code == error_code:
					sleep_time = min(sleep_time*2, 320)
				else:
					sleep_time = 5
			if sleep_time >= 3600:
				response.close()
				sys.stderr.write('Too long backoff time... Quiting...\n')
				sys.exit(1)
			error_code = e.code
			try:
				response.close()
			except UnboundLocalError:
				pass
			sys.stderr.write('Reconnecting after {0:.2f} seconds...\n'.format(sleep_time))
			time.sleep(sleep_time)
		except (urllib.URLError, ssl.SSLError, httplib.IncompleteRead), e:
			sys.stderr.write('URLError/SSLError: ' + time.strftime('%b %d, %Y %H:%M:%S', time.localtime()) + '\n')
			sys.stderr.write(str(e) + '\n')
			if error_code == -1:
				sleep_time = min(sleep_time+0.25, 16)
			else:
				sleep_time = 0.25
			error_code = -1
			try:
				response.close()
			except UnboundLocalError:
				pass
			sys.stderr.write('Reconnecting after {0:.2f} seconds...\n'.format(sleep_time))
			time.sleep(sleep_time)
	
if __name__ == '__main__':
	fetchsamples()
