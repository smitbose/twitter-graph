import MySQLdb
import json
import time
import following
import os
import tweepy
import logging
import datetime

USER_DIR = 'twitter-followings'


def minefriends(api, centre):
    while True:
        try:
            print("The user currently being added/checked", centre)
            conn = MySQLdb.connect("localhost", "root", "1234", "twitter_graph")
            cursor = conn.cursor()

            userfname = os.path.join(USER_DIR, str(centre) + '.json')
            if not os.path.exists(userfname):
                user = api.get_user(centre)
                time.sleep(60)
                sql_stmt = 'INSERT OR IGNORE INTO Politicians VALUES(%s,%s,%d)' % (
                    str(user.screen_name), str(user.location), user.followers_count)
                try:
                    cursor.execute(sql_stmt)
                    conn.commit()
                except:
                    conn.rollback()

                conn.close()

                following_names = following.get_following(api, centre)

                d = {'name': user.name,
                     'screen_name': user.screen_name,
                     'id': user.id,
                     'friends_count': user.friends_count,
                     'followers_count': user.followers_count,
                     'following_names': following_names}

                with open(userfname, 'w') as outf:
                    outf.write(json.dumps(d, indent=1))
                    outf.close()
                break
        except tweepy.TweepError as error:
            print(str(error))

            if str(error) == 'Not authorized.':
                print('Can''t access user data - not authorized.')
                break
            if str(error) == 'User has been suspended.':
                print('User suspended.')
                break
            if str(error) == "[{'message': 'Rate limit exceeded', 'code': 88}]" or str(error) == "[{u'message': " \
                                                                                                 "u'Rate limit " \
                                                                                                 "exceeded', " \
                                                                                                 "u'code': 88}]":
                print('Rate limited. Sleeping for 15 minutes.')
                logging.debug('Rate limit exceeded at %s' % str(datetime.now()))
                time.sleep(15 * 60 + 15)
        continue
