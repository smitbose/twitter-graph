import os
import tweepy
import time
import sys
import argparse
import json
import authenticate
import follower
import mentions
import logging


USER_DIR = 'twitter-followers'
MENTION_DIR = 'twitter-mentions'

seed = []

api = authenticate.start_auth()

# create a
def create_seed(init_file_name):

    # clearing the user and mention directories
    for the_file in os.listdir(USER_DIR):
        file_path = os.path.join(USER_DIR,the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)

    for the_file in os.listdir(MENTION_DIR):
        file_path = os.path.join(MENTION_DIR, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)

    # each line in f is a twitter username
    f = open(init_file_name,'r')
    logging.info('Reading initial file...')
    for line in f:
        id = line.split(' ',1)[0].strip()
        logging.info(str(id))
        seed.append(str(id))
    f.close()
    return seed


def start_collection(depth):

    for account in seed:
        follower.get_followers(api,account,depth,0)
        mentions.get_mentions(api,account)



if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-d","--depth",required=True,help="Depth upto which to traverse the follower list")
    ap.add_argument("-f","--initfile",required=True,help="Initial seed")


    args = vars(ap.parse_args())

    depth = int(args['depth'])
    f = args['initfile']

    print(depth)
    print(f)

    logging.basicConfig(filename='crawler_log.log',filemode='w',level=logging.DEBUG)

    create_seed(f)
    start_collection(depth)
