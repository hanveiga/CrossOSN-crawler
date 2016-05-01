# -*- coding: utf-8 -*-
import re
import sys
from collections import defaultdict
import cPickle as pickle
import csv
import time
import numpy as np
import urllib2
import oembed

import tweepy
from instagram.client import InstagramAPI

import check_remaining_calls as limit

import twitter_config as tconf
import instagram_config as iconf

consumer_key = tconf.consumer_key
consumer_secret = tconf.consumer_secret
access_token = tconf.access_token
access_token_secret = tconf.access_token_secret

def search_on_user(api, user_name, search_term):
    """ Searches a term over a user's twitter feed """
    limit.check_remaining_calls(api)
    c = tweepy.Cursor(api.search, q=search_term+ ' -RT' + ' from:'+user_name, lang="en") # Removes retweets
    limit.check_remaining_calls(api)
    list_of_tweets = []
    counter = 0
    for tweet in c.items():
        limit.check_remaining_calls(api)
        counter = counter + 1
        tweet_text = tweet.text
        regex = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
        match = re.search(regex, tweet_text)
        if match:
            link = match.group()
            list_of_tweets.append(link)
    if counter == 0:
        return 'null'

    return list_of_tweets[0]

def search_tweets_by_key(auth, xpost_term, xpost_term_2,filename):
    api = tweepy.API(auth)

    limit.check_remaining_calls(api)
    c = tweepy.Cursor(api.search, q=xpost_term + ' -RT' + ' lang:en', lang="en")
    limit.check_remaining_calls(api)

    # save nicknames
    csv_file = open(str(filename)+'usernames'+'.csv','wb')
    csv_writer = csv.writer(csv_file,delimiter=';')

    csv_ids = open(str(filename)+'userids'+'.csv','a')
    csv_ids_writer = csv.writer(csv_ids,delimiter=';')

    # save ids
    linking = []

    for tweet in c.items():
        try:
            limit.check_remaining_calls(api)
            tweet_text = tweet.text.encode('cp850', errors='replace').decode('cp850')
            regex = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
            match = re.search(regex, tweet_text)
            if match:
                link = match.group()
    	        limit.check_remaining_calls(api)
                response = search_on_user(api,tweet.user.screen_name,xpost_term_2)
                limit.check_remaining_calls(api)
                if response is 'null':
                    pass
                else:
                    try:
                        print 'Found instagram.'
                        instagram_user = get_insta_user(response)
                        print instagram_user
                        if len(instagram_user[0]) < 2:
                            print "Name too short, probably error."
                        else:
                            user = [tweet.user.screen_name,instagram_user[1],link]
                            userids = [tweet.user.id,instagram_user[0],link]
                            print 'User linked:'
                            print [tweet.user.screen_name,instagram_user[1],link]
                            linking.append(user)
                            csv_writer.writerow(user)
                            csv_ids_writer.writerow(userids)
                    except:
                        pass

            if len(linking)>=500: # just some limit of found users, used for testing code
                break
        except:
            pass

    csv_file.close()
    csv_ids.close()


def get_insta_user(short_link, debug=1):
    """ Get instagram userid from a link posted on twitter """
    print "Fetching instagram user. "
    try:
        response = urllib2.urlopen(short_link) # Some shortened url, eg: http://t.co/z8P2xNzT8k
        url_destination_https = response.url
        url_destination = url_destination_https.replace('https','http',1)

        # from link get the media_id
        consumer = oembed.OEmbedConsumer()
        endpoint = oembed.OEmbedEndpoint('https://api.instagram.com/oembed?url=', ['http://instagr.am/p/*'])
        consumer.addEndpoint(endpoint)
        media_id_code = re.split('/',url_destination)[-2]
        url_destination = 'http://instagr.am/p/'+media_id_code
        response = consumer.embed(url_destination)
        media_id = response['media_id']

        api = InstagramAPI(client_id=iconf.client_id, client_secret=iconf.client_secret)
    except:
            if debug:
                print 'Unable to find picture from link.'
            return 'null'

    try:
        media = api.media(media_id)
        return [media.user.id, media.user.username]
    except:
        if debug:
            print 'Unable to fetch instagram ID - most likely private user'
        return 'null'

if __name__=='__main__':
    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    for i in np.arange(1,100):
        try:
            search_tweets_by_key(auth, 'swarmapp.com','instagram.com', i)
        except:
            pass
