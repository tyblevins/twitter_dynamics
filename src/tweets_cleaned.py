import json
import re
import sys

# function to clean tweets and count number containing unicode
def clean_tweets(tweets_input,tweets_output):

	# read in tweets
	f = open(tweets_input,'r')
	tweets = f.readlines()

	# open output file for cleaned tweets
	ft1 = open(tweets_output,'w')

	# count of tweets with unicode
	uni_count = 0

	# clean tweets one by one
	for tweet in tweets:

		# fault tolerant (empty text or timestamp)
	    try:

	    	# load tweet to json and extract created_at and text values
	        tmp_tweet = json.loads(tweet)
	        time = tmp_tweet['created_at']
	        text = tmp_tweet['text']

	        # remove unicode from text
	        text_clean = re.sub(r'[^\x00-\x7f]',r'',text)


	        # count texts with unicode
	        if text_clean != text:
	            uni_count += 1

	        # clean escape characters
	        text_clean = text_clean.replace('\/','/')
	        text_clean = text_clean.replace('\n',' ')
	        text_clean = text_clean.replace('\t',' ')
	        text_clean = text_clean.strip()

	        # write tweet to file
	        ft1.write('%(tweet_text)s (timestamp: %(tweet_time)s)\n' % \
	                  {"tweet_text":text_clean, "tweet_time":time})

	    except:
	        KeyError

	# write the number of tweets with unicode and close file
	ft1.write('\n%d tweets contained unicode.' %uni_count)
	ft1.close()

# main
if __name__ == '__main__':
    
    # input and output files from run.sh command
    tweets_input = sys.argv[1]
    tweets_output = sys.argv[2]

    #compute average degree of hashtags in tweets
    clean_tweets(tweets_input,tweets_output)