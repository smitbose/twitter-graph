import os
import tweepy
import time
import sys
import argparse
import json
import authenticate
import follower
import mentions


seed = []

api = authenticate.start_auth()

# create a
def create_seed(init_file_name):

    # each line in f is a twitter username
    f = open(init_file_name,'r')
    for line in f:
        id = line.split(' ',1)[0]
        print(id)
        seed.append(line.split(' ',1)[0])

    return seed


def start_collection(depth):

    for account in seed:
        follower.get_followers(api,account,depth,0)
        #mentions.mine_mentions(account)



if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-d","--depth",required=True,help="Depth upto which to traverse the follower list")
    ap.add_argument("-f","--initfile",required=True,help="Initial seed")


    args = vars(ap.parse_args())

    depth = int(args['depth'])
    f = args['initfile']

    print(depth)
    print(f)

    create_seed(f)
    start_collection(depth)
