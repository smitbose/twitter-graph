import os
import tweepy
import time
import sys
import argparse
import json
import authenticate
import following
import mentions
import logging

USER_DIR = 'twitter-following'
MENTION_DIR = 'twitter-mentions'

seed = []

api = authenticate.start_auth()


# create a
def create_seed(init_file_name):

    if not os.path.exists(USER_DIR):
        os.mkdir(USER_DIR)
    if not os.path.exists(MENTION_DIR):
        os.mkdir(MENTION_DIR)

    # clearing the user and mention directories
    for the_file in os.listdir(USER_DIR):
        file_path = os.path.join(USER_DIR, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)

    for the_file in os.listdir(MENTION_DIR):
        file_path = os.path.join(MENTION_DIR, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)

    # each line in f is a twitter username
    # noinspection PyShadowingNames
    f = open(init_file_name, 'r')
    logging.info('Reading initial file...')
    for line in f:
        # noinspection PyShadowingBuiltins
        id = line.split(' ', 1)[0].strip()
        logging.info(str(id))
        seed.append(str(id))
    f.close()
    return seed


def start_collection(depth):
    for account in seed:
        following.get_following(api, account, depth, 0)
        mentions.get_mentions(api, account)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()

    ap.add_argument('-f','--file',required=True,help='The file that contains the base accounts')
    ap.add_argument('-d','--depth',required=True,help='The depth to which the following list will be mined')

    args = vars(ap.parse_args())

    basefilename = args['file']
    depth = args['depth']

    # initialize logger
    logging.basicConfig(filename='crawler_log.log', filemode='w', level=logging.DEBUG)

    create_seed(basefilename)
    start_collection(depth)