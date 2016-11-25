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


seed = []

api = authenticate.start_auth()

# create a
def create_seed(init_file_name):

    # each line in f is a twitter username
    f = open(init_file_name,'r')
    logging.info('Reading initial file...')
    for line in f:
        id = line.split(' ',1)[0]
        logging.info(str(id))
        seed.append(id)

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
