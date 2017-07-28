"""
This CLI utilizes the Tweepy Python wrapper for twitter

Arguments passed:
    handle:         Twitter handle
    tweet_count:    Count of tweets (max of 20) 
"""
# -*- coding: utf-8 -*-
import argparse
import sys
import tweepy


def arg_setup():
    """ 
    Command Line Argument setup and integration
    
    Sets up Command Line arguments and helpful information for the user,
    then parses the arguments given and saves them as attributes of a 
    created Namespace. These can be retrieved by name using the dot operator
    in conjunction with the [args] variable.
    
    Parameters
    ----------
    N/A
        No input
        
    Returns
    -------
    Namespace object
        Namespace object with argument-to-attribute population
    """

    parser = argparse.ArgumentParser(description='This program displays 1-20 tweets for a twitter user')
    parser.add_argument("handle", help='twitter handle (pass with or without \'@\' symbol)')
    parser.add_argument("tweet_count", type=int, help='number of tweets to display (max of 20)')
    args = parser.parse_args()

    # Allow for optional @ symbol in twitter handle
    if '@' in args.handle:
        args.handle = args.handle.translate(None, '@')

    return args


def auth_setup():
    """ 
    Tweepy Authorization Setup
    
    Gets the auth tokens and keys; user should have their own consumer key and consumer secret.
    Parameters
    ----------
    N/A
        No input
        
    Returns
    -------
    auth
        Object containing access tokens
    """

    # Grab consumer token and secret from user, start handshake
    consumer_token = input("Please enter your consumer token: ")
    consumer_secret = input("Please enter your consumer secret: ")
    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    auth.secure = True

    # Supply request token and url
    try:
        auth_url = auth.get_authorization_url()
        print("Please visit this url to authorize the app: \n{}\nPlease enter the Auth PIN"
              .format(auth_url))
    except tweepy.TweepError:
        print("Request token retrieval failed...")

    # Retrieve auth pin from user, get and set access token
    auth_pin = input().strip()
    access_token = auth.get_access_token(verifier=auth_pin)
    auth.set_access_token(access_token[0], access_token[1])

    # (optional)Create tokens for user for future use
    # with open("Tokens", "w") as f: f.write('{}\n{}\n'.format(access_token[0], access_token[1])

    return auth


def display_tweets(args):
    """ # Get [tweet_count] tweets for [handle]"""
    tweets = api.user_timeline(args.handle, count=args.tweet_count)
    for tweet in tweets:
        print(tweet.text.encode(sys.stdout.encoding, errors='replace'))


if __name__ == '__main__':
    cli_args = arg_setup()
    tweepy_auth = auth_setup()
    api = tweepy.API(tweepy_auth)
    display_tweets(cli_args)

