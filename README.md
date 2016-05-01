# CrossOSN
Cross Online social Network Crawler to link users from Twitter, Instagram and Foursquare.

## What do the scripts do:

__find_users.py__ searches through Twitter for users who crossposted Instagram and Foursquare content and outputs a csv file with the user ids on Instagram and Twitter. The Foursquare ID is not given because the Foursquare API doesn't let you fetch users, but the users in the list have posted content from Foursquare.

__fetch_data.py__ provides routines to fetch profile and user media when given user ids from instagram and twitter, and ids from media from twitter, instagram and foursquare

__read_data.py__ routines that read data of the format given in 'sample_data'

__make_dataset.py__ reads output from read_data.py and assembles data from users

## How to run the scripts
Best way is to get the code running quickly using virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/

Then run:

```pip install -r requirements.txt```

## Dataset
To get a snapshot of the dataset from February 2016 that you can create with these scripts, feel free to email han.veiga@gmail.com
