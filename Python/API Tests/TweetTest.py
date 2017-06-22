import tweepy
from keys import *

auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

api = tweepy.API(auth)
me = api.me()
# print user
# print api.saved_searches()

print('My Name: ' + me.name)
print('My Location: ' + me.location)
print('My Friends: ' + str(me.friends_count))
print('My Screen Name: ' + me.screen_name)

mom = api.get_user('Debnheirs')
print('Mom\'s name: ' + mom.name)
print('Mom\'s location: ' + mom.location)
print('Mom\'s image is: ' + mom.profile_image_url)

myTimeline = api.home_timeline(count = 3)
for tweets in myTimeline:
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
myStream.filter(track=['deborah'])
