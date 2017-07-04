"""
    This CLI utilizes the Tweepy Python wrapper for twitter
    
    Arguments passed:
        handle:         Twitter handle
        tweet_count:    Count of tweets (max of 20) 
"""
# -*- coding: utf-8 -*-
import argparse
import tweepy
from keys import *

import sys

# set up arguments and helpful information for user
parser = argparse.ArgumentParser(description='This program displays 1-20 tweets for a twitter user')
parser.add_argument("handle", help='twitter handle (pass with or without \'@\' symbol)')
parser.add_argument("tweet_count", type=int, help='number of tweets to display (max of 20)')
args = parser.parse_args()

if '@' in args.handle: args.handle = args.handle.translate(None, '@')

# Get auth tokens and keys, as long as user has defined their own ckey and csecret
auth = tweepy.OAuthHandler(ckey, csecret)
auth.secure = True
authUrl = auth.get_authorization_url()

# grab auth pin for user
print("Please visit this url to authorize the app:")
print(authUrl)
print("Please enter the Auth PIN: ")

authPIN = raw_input().strip()
token = auth.get_access_token(verifier=authPIN)
auth.set_access_token(token[0], token[1])

# create tokens for user for future use (optional)
accessTokenFile = open("Tokens", "w")
accessTokenFile.write(token[0] + '\n')
accessTokenFile.write(token[1] + '\n')

api = tweepy.API(auth)

# get [tweet_count] tweets for [handle]
tweets = api.user_timeline(args.handle, count=args.tweet_count)
for tweet in tweets:
    print tweet.text.encode(sys.stdout.encoding, errors='replace')
