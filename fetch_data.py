# -*- coding: utf-8 -*-
import re
import sys
import time
import datetime
import random
import os.path
import cPickle as pickle

from instagram.client import InstagramAPI
import tweepy
import check_remaining_calls as limit

### TWITTER API
import twitter_config as tconf
consumer_key = tconf.consumer_key
consumer_secret = tconf.consumer_secret
access_token = tconf.access_token
access_token_secret = tconf.access_token_secret

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api_twitter = tweepy.API(auth)

### INSTAGRAM API
import instagram_config as iconf
api_instagram = InstagramAPI(client_id=iconf.client_id, client_secret=iconf.client_secret)

### FOURSQUARE API
import foursquare
import foursquare_config as fconf

# Construct the client object
api_foursquare = foursquare.Foursquare(client_id=fconf.client_id, client_secret=fconf.client_secret)

def fetch_tweet(tweet_id):
	return api_twitter.get_status(tweet_id)

def fetch_instaphoto(media_id):
	return api_instagram.media(media_id)

def fetch_twitter_user(twitter_id):
	return api_twitter.get_user(twitter_id)

def fetch_instagram_user(instagram_id):
	return api_instagram.user(user_id=instagram_id)

def fetch_foursquare_venue(venue_id):
	return api_foursquare.venues(venue_id)

