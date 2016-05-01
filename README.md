# CrossOSN
Cross Online social Network Crawler to link users from Twitter, Instagram and Foursquare.

## What do the scripts do:

__find_users.py__ searches through Twitter for users who crossposted Instagram and Foursquare content and outputs a csv file with the user ids on Instagram and Twitter. The Foursquare ID is not given because the Foursquare API doesn't let you fetch users, but the users in the list have posted content from Foursquare.

__fetch_user_data.py__ grabs the profiles and timelines of a list of users or of a list of tweets/instagram posts/foursquare check ins.

## How to run the scripts
Best way is to install virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/

Then run:

```pip install -r requirements.txt```

