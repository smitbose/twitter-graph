import sqlite3
import json
import time
import following
import os

USER_DIR = 'twitter-followings'

def minefriends(api,centre):

    print("The user currently being added/checked",centre)
    conn = sqlite3.connect('doge.sql')
    conn.execute('''CREATE TABLE IF NOT EXISTS Politicians(UserName text,Location text,FollowerCount int,PRIMARY KEY
    (UserName))''')

    userfname = os.path.join(USER_DIR,str(centre)+'.json')
    if not os.path.exists(userfname):
        user = api.get_user(centre)
        time.sleep(60)
        conn.execute('INSERT OR IGNORE INTO Politicians VALUES(?,?,?)', (user.screen_name, user.location, user.followers_count))
        conn.commit()
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