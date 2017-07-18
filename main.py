# >>> sources:
# https://miguelmalvarez.com/2015/03/03/download-the-pictures-from-a-twitter-feed-using-python/
# https://marcobonzanini.com/2016/08/02/mastering-social-media-mining-with-python/
# http://tkang.blogspot.co.uk/2011/01/tweepy-twitter-api-status-object.html

import tweepy
from tweepy import OAuthHandler
import json
import wget

consumer_key = 'your consumer key'
consumer_secret = 'your consumer secret'
access_token = 'your access token'
access_secret = 'your access secret'

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

# Status() is the data model for a tweet
tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse
# User() is the data model for a user profil
tweepy.models.User.first_parse = tweepy.models.User.parse
tweepy.models.User.parse = parse
# You need to do it for all the models you need

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

handl = raw_input("Twitter handle: ")
cnt = int(raw_input("How many tweets? "))
hashtag = raw_input("What hashtag are we looking for? Press enter if none. ").lower()
tweets = api.user_timeline(screen_name=handl,
                           count=cnt, include_rts=True,
                           exclude_replies=False)
media_files = set()
for status in tweets:

    media = status.entities.get('media', [])

    if(len(media) > 0) & (hashtag in status.text.lower()):
        media_files.add(media[0]['media_url'])
        print '\n\n >>> Tweet: ' , status.text


if media:
    print 'Downloading the images: '
    for media_file in media_files:
        print media_file
        wget.download(media_file)

print '\nDONE!'
