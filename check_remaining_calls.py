# -*- coding: utf-8 -*-
import time

def check_remaining_calls(api_twitter):
    try:
	#remaining = int(api_twitter.last_response.getheader('x-rate-limit-remaining'))
        remaining = int(api_twitter.last_response.headers['x-rate-limit-remaining']) #updated package, compatible with Tweepy 3.2.0
	if remaining <= 5:
            print "Remaining calls exhausted: Entered sleep period."
            time.sleep(15*60 + 10) # Wait 15 minutes - Twitter limits
            print "Remaining calls replendished: Exited sleep period."
            U = api_twitter.get_user(screen_name='hanveiga') # Resetting the counter
                                                             # If we don't ping the server again we don't get the resetted response.
        else:
            pass

    except:
        print 'Exception: There is no last response yet.'