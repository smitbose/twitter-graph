import os
import time
import tweepy
import csv
import logging
from datetime import datetime

USER_DIR = 'twitter-mentions'


def get_mentions(api, screen_name):
    userfname = os.path.join(USER_DIR, str(screen_name) + '.csv')
    if not os.path.exists(userfname):
        while True:
            try:

                alltweets = []
                new_tweets = api.user_timeline(screen_name=screen_name, count=200, include_rts=True)
                # saves the first 200 tweets
                alltweets.extend(new_tweets)

                # saves the id of the oldest tweet
                oldest = alltweets[-1].id - 1

                fhandle = open(userfname, 'w')
                # file handle to dump the mention
                count = 0
                # keep grabbing tweets until there are no tweets left to grab
                while len(new_tweets) > 0 and count < 5:
                    print("getting %s next set of tweets..." % str(count))
                    logging.info("getting %s next set of tweets" % str(count))

                    # all subsequent requests use the max_id param to prevent duplicates
                    new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest, include_rts=True)

                    # save most recent tweets
                    alltweets.extend(new_tweets)

                    # update the id of the oldest tweet less one
                    oldest = alltweets[-1].id - 1

                    print("...%s tweets downloaded so far" % (len(alltweets)))
                    count += 1

                writer = csv.writer(fhandle)
                for tweets in alltweets:
                    str_tweets = str(tweets.text)
                    date = tweets.created_at
                    if str_tweets.startswith('RT'):
                        tweet = str_tweets.split()
                        retweet = tweet[1][1:].rstrip(',.:;!')

                        writer.writerow([retweet, str(date.date()), str(date.time())])
                    else:
                        # date of tweets and each mention is collected
                        for tweet in str_tweets.split():
                            tweet.strip()
                            if tweet[0] == '@':
                                mention = tweet[1:].rstrip(',.:;!')

                                writer.writerow([mention, str(date.date()), str(date.time())])
                fhandle.close()
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
        return
