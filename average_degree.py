import json
import re
import time as tim
import datetime
import json
import itertools

# function to clean unicode from text
def clean(text):
    text_clean = re.sub(r'[^\x00-\x7f]',r'',text)
    return text_clean

# function to convert JSON time to timestamp
def time2timestamp(time):
    time = datetime.datetime.fromtimestamp(tim.mktime(tim.strptime(time, "%a %b %d %H:%M:%S +0000 %Y")))
    return time


# unit tests
# apachehashtags = [['insight','spark'],['trump','election','spark'],['insight','apache','hadoop'],['official','jealous','trump','spark'],['tacky','bathroom','trump'],['insight','python','spark'],['cassandra','spark','hurrdoncare'],['trump','django','hurrdoncare'],['editor','spark','pop'],['trump','hadoop','pop']]
# apachetimes = ["Fri Oct 30 15:32:56 +0000 2015","Fri Oct 30 15:33:15 +0000 2015","Fri Oct 30 15:33:30 +0000 2015","Fri Oct 30 15:33:45 +0000 2015","Fri Oct 30 15:34:00 +0000 2015","Fri Oct 30 15:34:15 +0000 2015","Fri Oct 30 15:34:30 +0000 2015","Fri Oct 30 15:34:45 +0000 2015","Fri Oct 30 15:35:00 +0000 2015","Fri Oct 30 15:35:15 +0000 2015"]

def avg_deg(tweets_input,tweets_output):
    
    # initialize data structs
    # array of lists, where each list is a tweet's hashtags and time
    tweetd = []

    # adjacency dictionary for each hashtag
    nodes = {}
    
    # read in tweets
    f = open(tweets_input,'r')
    tweets = f.readlines()

    # open output file for rolling average
    ft2 = open(tweets_output,'w')
    
    # loop through tweets
    for idx,tweet in enumerate(tweets):

        # convert to JSON format
        twt = json.loads(tweet)

        # fault tolerant for no hashtag field
        try:

            # extract hashtag information
            hashtags = twt['entities']['hashtags']
            

            # extract hashtag text, clean, and make lowercase
            tags = [(clean(hashtag['text'])).lower() for hashtag in hashtags]

            # remove empty hashtags
            tags = [tag for tag in tags if tag != u'']

            # extract time and convert to timestamp
            time = time2timestamp(twt['created_at'])

            # append tweet time and associated hashtags to tweetd array
            tweetd.append([time,tags])

            # add hashtags to dictionary or modify existing keys, given more than one hashtag in tweet
            if len(tags) > 1:
                perms = itertools.permutations(tags,2)
                for perm in perms:
                    if(perm[0] in nodes.keys()):
                        nodes[perm[0]].append(perm[1])
                    else:
                        nodes[perm[0]] = [perm[1]]


            # time difference between newest tweet and oldest tweet still under consideration
            tdiff = (tweetd[-1][0] - tweetd[0][0]).total_seconds()

            # eject tweets not in 60 second window
            while tdiff > 60:

                # hastags from tweet to eject
                tags_to_pop = tweetd[0][1]

                # Get all pairwise edges for the tweet to be popped
                perms = itertools.permutations(tags_to_pop,2)

                # For each hashtag, remove from dictionary values. 
                # If hashtag key has no values (node with no edges), remove key from dictionary.
                for perm in perms:
                    
                    if(perm[0] in nodes.keys()):
                        if(perm[1] in nodes[perm[0]]):
                            nodes[perm[0]].pop(nodes[perm[0]].index(perm[1]))
                            if(len(nodes[perm[0]]) == 0):
                                nodes.pop(perm[0],None)
                        else:
                            print 'corrupted adjacency dictionary - values'
                            raise

                    else:
                        print 'corrupted adjacency dictionary - keys'
                        raise
                # pop old tweet
                tweetd = tweetd[1:]

                # recalculate time distance for next oldest tweet
                tdiff = (tweetd[-1][0] - tweetd[0][0]).total_seconds()


            # take average value
            sm = 0
            for ends in nodes.values():
                sm += len(set(ends))*1.0/len(nodes.values())
            avg = sm

            # write avg to file with 2 digit precision
            ft2.write('%(average).2f\n' % \
                      {"average":avg})
        except:
            KeyError

    # close file
    ft2.close()

# main
if __name__ == '__main__':
    
    # input and output files from run.sh command
    tweets_input = sys.argv[2]
    tweets_output = sys.argv[3]

    #compute average degree of hashtags in tweets
    avg_deg(tweets_input,tweets_output)






