import csv
from collections import defaultdict
import sys

import fetch_data as fd

""" Read files of the format given in sample data and dumps a pickle """

def read_user_data(user_csv,tweets_list=None,instagram_list=None,foursquare_list=None):

	if tweets_list is not None:
		tweets_per_user = defaultdict(list)
		# If list of format user_id, tweets is provided
		# we include these tweets on the UserTriple data
		try:		
			twitter_data = csv.reader(open(tweets_list,'rb'))
			# store a defaultdict(list) of user-id and tweetids
			twitter_data.skip()
			for row in twitter_data:
				user_id, tweet_id = row
				tweets_per_user[user_id].append(tweet_id)
		except:
		    print "Unexpected error:", sys.exc_info()[0]
		    raise

	if instagram_list is not None:
		instagram_per_user = defaultdict(list)
		try:		
			instagram_data = csv.reader(open(instagram_list,'rb'))
			instagram_data.next()
			for row in instagram_data:
				user_id, photo_id = row
				instagram_per_user[user_id].append(photo_id)
		except:
		    print "Unexpected error:", sys.exc_info()[0]
		    raise

	if foursquare_list is not None:
		fourquare_per_user = defaultdict(list)
		try:		
			foursquare_data = csv.reader(open(foursquare_lists,'rb'))
			foursquare_data.next()
			for row in foursquare_data:
				user_id, tweet_id, checkin_id = row
				foursquare_per_user[user_id].append([tweet_id,checkin_id])
		except:
		    print "Unexpected error:", sys.exc_info()[0]
		    raise


	with open(csv_file,'rb') as user_csv:
		userdata = csv.reader(csvfile)
		userdata.next() #header
		for row in userdata:
			twitter_id, instagram_id, foursquare_id, spammer = row
			twitter_profile = fd.fetch_twitter_user(twitter_id)
			instagram_profile = fd.fetch_instagram_user(instagram_id)
			user = UserTriplet(twitter_profile,instagram_profile)

			if not twitter_per_user[twitter_id]:
				user.fetch_list_tweets(twitter_per_user[twitter_id])

			if not instagram_per_user[instagram_id]:
				user.fetch_list_instagram(instagram_per_user[instagram_id])

			if not fourquare_per_user[twitter_id]:
				user.fetch_list_foursquare(fourquare_per_user[twitter_id])


			pickle.dump(open(twitter_id+'.pkl','wb'),user)


class UserTriplet(object):
	def __init__(self,twitter,instagram):
		self.twitter_profile = twitter
		self.instagram_profile = instagram
		self.twitter_timeline = []
		self.instagram_timeline = []
		self.foursquare_timeline = []

	def fetch_list_tweets(self,t_list):
		for tweet in t_list:
			self.twitter_timeline.append(fs.fetch_tweet(tweet))

	def fetch_list_instagram(self,i_list):
		for photo in i_list:
			self.instagram_timeline.append(fs.fetch_instaphoto(photo))

	def fetch_list_foursquare(self,i_list):
		for entry in i_list:
			self.foursquare_timeline.append([fs.fetch_tweet[entry[0], \
				fs.fetch_foursquare_venue(entry[1])])


	def get_new_tweets(self):
		pass

	def get_new_instagram_posts(self):
		pass

if __name__=='__main__':
	read_user_data(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])