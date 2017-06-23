'''
    This CLI utilizes the Tweepy Python wrapper for twitter
    
    Arguments passed:
        handle:         Twitter handle
        tweet_count:    Count of tweets (max of 20) 
'''
# -*- coding: utf-8 -*-
import argparse
import tweepy
from keys import *

import sys

parser = argparse.ArgumentParser(description='This program displays 1-20 tweets for a twitter user')
parser.add_argument("handle", help='twitter handle (pass with or without \'@\' symbol)')
parser.add_argument("tweet_count", type=int, help='number of tweets to display (max of 20)')
args = parser.parse_args()

if '@' in args.handle: args.handle = args.handle.translate(None, '@')

auth = tweepy.OAuthHandler(ckey, csecret)
auth.secure = True
authUrl = auth.get_authorization_url()

print("Please visit this url to authorize the app:")
print(authUrl)
print("Please enter the Auth PIN: ")

authPIN = raw_input().strip()
token = auth.get_access_token(verifier=authPIN)
auth.set_access_token(token[0], token[1])

accessTokenFile = open("Tokens", "w")
accessTokenFile.write(token[0] + '\n')
accessTokenFile.write(token[1] + '\n')

api = tweepy.API(auth)

tweets = api.user_timeline(args.handle, count=args.tweet_count)
for tweet in tweets:
    print tweet.text.encode(sys.stdout.encoding, errors='replace')
