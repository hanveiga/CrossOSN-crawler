import csv
from collections import defaultdict
import sys
import cPickle as pickle
import os
import json
import shutil

import fetch_data as fd
import crawl_website as crawl

def read_twitter_data(twitter_csv,path=''):
	path=path+'/'
	with open(twitter_csv,'r') as csvfile:
		userdata = csv.reader(csvfile)
		userdata.next() #header
		users = []

		for row in userdata:
			twitter_id, tweet_id = row
			if twitter_id not in users:
				save_to_path = '{path}{id1}{id2}/'.format(path=path,id2=twitter_id+'_twitter',id1=twitter_id+'/')
				#os.makedirs(save_to_path)
				make_dir(save_to_path)
				twitter_profile = fd.fetch_twitter_user(twitter_id)
				json.dump(twitter_profile._json, open(save_to_path+twitter_id+'.json', 'w'))
				users.append(twitter_id)
				save_to_path_2 = '{path}{id1}{id2}/tweets'.format(path=path,id2=twitter_id+'_twitter',id1=twitter_id+'/')
				#os.makedirs(save_to_path_2)
				make_dir(save_to_path_2)

			# check if file exists
			if check_file_exists(save_to_path_2+'/'+tweet_id+'.json'): # if true
				pass
			else:
				tweet = fd.fetch_tweet(tweet_id)
				json.dump(tweet._json, open(save_to_path_2+'/'+tweet_id+'.json', 'w'))

def read_instagram_data(instagram_csv,path=''):
	path = path + '/'
	# mapping between user twitter and instagram
	map_tw_inst = {}
	with open('users_linked.csv','r') as userscsv:
		userlink = csv.reader(userscsv)
		userlink.next() #header
		users_linked = []
		for row in userlink:
			tw_id, ins_id, fqs_id, spam = row
			map_tw_inst[ins_id] = tw_id

	with open(instagram_csv,'r') as csvfile:
		userdata = csv.reader(csvfile)
		userdata.next() #header
		users = []

		for row in userdata:
			inst_id, photo_id = row
			if inst_id not in users:
				save_to_path = '{path}{id1}{id2}/'.format(path=path,id2=map_tw_inst[inst_id]+'_instagram',id1=map_tw_inst[inst_id]+'/')
				#os.makedirs(save_to_path)
				make_dir(save_to_path)
				inst_profile = fd.fetch_instagram_user(inst_id)
				json.dump(inst_profile._json, open(save_to_path+inst_id+'.json', 'w'))
				users.append(inst_id)
				save_to_path_2 = '{path}{id1}{id2}/photos'.format(path=path,id2=map_tw_inst[inst_id]+'_instagram',id1=map_tw_inst[inst_id]+'/')
				#os.makedirs(save_to_path_2)
				make_dir(save_to_path_2)

			if check_file_exists(save_to_path_2+'/'+photo_id+'.json'):
				pass
			else:
				photo = fd.fetch_instaphoto(photo_id)
				json.dump(photo._json, open(save_to_path_2+'/'+photo_id+'.json', 'w'))

def read_instagram_data_no_api(instagram_csv,path=''):
	path = path + '/'
	# mapping between user twitter and instagram
	map_tw_inst = {}
	with open('users_linked.csv','r') as userscsv:
		userlink = csv.reader(userscsv)
		userlink.next() #header
		users_linked = []
		for row in userlink:
			tw_id, ins_id, fqs_id, spam = row
			map_tw_inst[ins_id] = tw_id

	with open(instagram_csv,'r') as csvfile:
		userdata = csv.reader(csvfile)
		userdata.next() #header
		users = []

		for row in userdata:
			inst_id, photo_id = row
			if inst_id not in users:
				save_to_path = '{path}{id1}{id2}/'.format(path=path,id2=map_tw_inst[inst_id]+'_instagram',id1=map_tw_inst[inst_id]+'/')
				#os.makedirs(save_to_path)
				make_dir(save_to_path)
				users.append(inst_id)
				save_to_path_2 = '{path}{id1}{id2}/photos'.format(path=path,id2=map_tw_inst[inst_id]+'_instagram',id1=map_tw_inst[inst_id]+'/')
				#os.makedirs(save_to_path_2)
				make_dir(save_to_path_2)

			if check_file_exists(save_to_path_2+'/'+photo_id+'.json'):
				pass
			else:
				url = 'https://instagram.com/p/'+photo_id
				photo = crawl.crawl_photo(url)
				json.dump(photo, open(save_to_path_2+'/'+photo_id+'.json', 'w'))

def read_foursquare_data(foursquare_csv, path=''):
	path = path + '/'
	with open(foursquare_csv,'r') as csvfile:
		userdata = csv.reader(csvfile)
		userdata.next() #header
		users = []

		for row in userdata:
			twitter_id, tweet_id, venue_id = row
			if twitter_id not in users:
				save_to_path = '{path}{id1}{id2}/'.format(path=path,id2=twitter_id+'_foursquare',id1=twitter_id+'/')
				#os.makedirs(save_to_path)
				make_dir(save_to_path)
				users.append(twitter_id)
				save_to_path_2 = '{path}{id1}{id2}/checkins'.format(path=path,id2=twitter_id+'_foursquare',id1=twitter_id+'/')
				#os.makedirs(save_to_path_2)
				make_dir(save_to_path_2)

			if check_file_exists(save_to_path_2+'/'+tweet_id+'_venue.json'):
				pass
			else:
				venue = fd.fetch_foursquare_venue(venue_id)
				json.dump(venue, open(save_to_path_2+'/'+tweet_id+'_venue.json', 'w'))

			if check_file_exists(save_to_path_2+'/'+tweet_id+'_tweet.json'):
				pass
			else:
				tweet = fd.fetch_tweet(tweet_id)
				json.dump(tweet._json, open(save_to_path_2+'/'+tweet_id+'_tweet.json', 'w'))

def crawl_dataset():
	# make user folder, populate with all data
	# make user folder 2
	# create dataset folder
	inst_no_access=0
	dataset = 'dataset_new'
	#os.makedirs(dataset)
	make_dir(dataset)
	with open('users_linked.csv','r') as csvfile:
		userdata = csv.reader(csvfile)
		userdata.next() #header
		users = []
		for row in userdata:
			twitter_id, instagram_id, foursquare_id, spammer = row
			if spammer==1:
				continue
			if twitter_id not in users:
				#os.mkdir(dataset+'/'+twitter_id) # index users by twitter id
				path = dataset+'/'+twitter_id
				make_dir(path)
				users.append(twitter_id)
			if len(users)>2:
				break
	# fill user folder
	read_foursquare_data('user_4sqcheckins.csv',path=dataset)
	read_twitter_data('user_tweets.csv',path=dataset)
	try:
		read_instagram_data('user_instaphotos.csv',path=dataset)
	except:
		read_instagram_data_no_api('user_instaphotos.csv',path=dataset)

def make_dir(path):
	if not os.path.exists(path):
	    os.makedirs(path)
	else:
	    #shutil.rmtree(path)        #removes all the subdirectories!
	    #os.makedirs(path)
		pass

def check_file_exists(path):
	if os.path.isfile(path):
		return 1
	else:
		return 0

if __name__=='__main__':
	print 'Instructions of use:'
	print 'Populate the files ...'
	print 'Run this script in the folder with the .csv files provided for the dataset'

	crawl_dataset()
	#fetch_functions = {'twitter': fd.fetch_tweet,
	#				   'instagram': fd.fetch_instaphoto}
	#
	#read_data(sys.argv[1], 'twitter', fetch_functions['twitter'])
	#read_twitter_data(sys.argv[1])
