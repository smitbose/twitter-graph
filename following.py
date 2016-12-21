import tweepy
import time
from datetime import datetime
import logging


def get_following(api,centre):

    following = []
    while True:
        try:
            i = 1
            for friends in tweepy.Cursor(api.friends,screen_name=centre,count=200).items():
                # print i,friends.screen_name
                i = i+1
                following.append(friends.screen_name)
                if i % 200 == 0:
                    time.sleep(60)
            break
        except tweepy.TweepError as error:
            print(str(error))

            if str(error) == 'Not authorized.':
                print('Can''t access user data - not authorized.')
                break
            if str(error) == 'User has been suspended.':
                print('User suspended.')
                break
            if str(error) == "[{'message': 'Rate limit exceeded', 'code': 88}]" or str(error) == "[{u'message': u'Rate limit exceeded', u'code': 88}]":
                print('Rate limited. Sleeping for 15 minutes.')
                logging.debug('Rate limit exceeded at %s' % str(datetime.now()))
                time.sleep(15 * 60 + 15)
        continue

    return following