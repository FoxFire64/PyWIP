import tweepy
from keys import *

if __name__ == "__main__":
    # get them keys, yo
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

    api = tweepy.API(auth)
    me = api.me()
    # print user
    # print api.saved_searches()

    print('My Name: ' + me.name)
    print('My Location: ' + me.location)
    print('My Friends: ' + str(me.friends_count))
    print('My Screen Name: ' + me.screen_name)

    my_timeline = api.home_timeline(count = 3)
    for tweets in my_timeline:
        print tweets.text

    #for friend in tweepy.Cursor(api.friends).items():
    #    print friend.name


    class StdOutListener(tweepy.StreamListener):
        def on_status(self, status):
            print('Text: ' + status.text)

            return True

        def on_error(self, status_code):
            print('Got an error with status code: ' + str(status_code))
            return True

        def on_timeout(self):
            print('Timeout...')
            return True


    StdOutListener = StdOutListener()
    myStream = tweepy.Stream(auth=api.auth, listener=StdOutListener)
    myStream.filter(track=['acacia'])
