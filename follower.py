import os
import time
import json
import tweepy

USER_DIR = 'twitter-followers'

def get_followers(api,centre, max_depth=1, current_depth=0):


    if current_depth > max_depth:
        return

    userfname = os.path.join(USER_DIR,str(centre)+'.json')

    if not os.path.exists(userfname):
        #mine follower list for user

        print('Retrieving details for user %s' % str(centre))

        while True:
            try:
                user = api.get_user(centre)

                followers = tweepy.Cursor(api.followers,screen_name=centre).items()

                print(user.name)

                follower_names = []

                for id in followers:
                    follower_names.append(id.screen_name)

                d = {'name': user.name,
                     'screen_name': user.screen_name,
                     'id': user.id,
                     'friends_count': user.friends_count,
                     'followers_count': user.followers_count,
                     'followers_ids': follower_names}

                with open(userfname,'w') as outf:
                    outf.write(json.dumps(d,indent=1))

                for follower in follower_names:
                    get_followers(api,follower,max_depth,current_depth+1)

                break
            except tweepy.TweepError as error:
                print(str(error))

                if str(error) == 'Not authorized.':
                    print('Can''t access user data - not authorized.')

                if str(error) == 'User has been suspended.':
                    print('User suspended.')

                if str(error) == "[{'message': 'Rate limit exceeded', 'code': 88}]" or str(error) == "[{'code': 88, 'message': 'Rate limit exceeded'}]":
                    print('Rate limited. Sleeping for 15 minutes.')
                    time.sleep(15 * 60 + 15)
            continue

    else:
        print("User %s already mined" % str(centre))