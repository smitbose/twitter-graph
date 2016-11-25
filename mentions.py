# -*- coding: utf-8 -*-
import os
import time
import json
import tweepy
import csv
from collections import Counter
from datetime import datetime
import logging

USER_DIR = 'twitter-mentions'

def get_mentions(api,screen_name):

    alltweets = []
    userfname = os.path.join(USER_DIR, str(screen_name) + '.csv')
    if not os.path.exists(userfname):
        print('Retrieving mentions for user %s' % str(screen_name))
        while True:
            try:

                new_tweets = api.user_timeline(screen_name=screen_name, count=200)

                alltweets.extend(new_tweets)

                mentions = []
                for tweets in alltweets:
                    for tweet in tweets.text.split():
                        if tweet.startswith('@'):
                            mentions.append(tweet[1:].rstrip(',.:;!'))

                dict = Counter(mentions)

                with open(userfname, 'w') as outf:
                    writer = csv.writer(outf)
                    for key,val in dict.items():
                        writer.writerow([key, val])
                break

            except tweepy.TweepError as error:
                print(str(error))

                if str(error) == 'Not authorized.':
                    print('Can''t access user data - not authorized.')
                    break
                if str(error) == 'User has been suspended.':
                    print('User suspended.')
                    break
                if str(error) == "[{'message': 'Rate limit exceeded', 'code': 88}]" or str(
                        error) == "[{'code': 88, 'message': 'Rate limit exceeded'}]":
                    print('Rate limited. Sleeping for 15 minutes.')
                    logging.debug('Rate limit exceeded at %s' % str(datetime.now()))
                    time.sleep(15 * 60 + 15)
    else:
        print("User %s already mined" % str(screen_name))
