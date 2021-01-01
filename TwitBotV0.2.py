#!/usr/bin/env python3

import time
import tweepy
import webbrowser

'''These are my developer keys'''
with open("keys.txt", "r") as f:
    keys = f.readlines()
consumer_key = str(keys[0]).strip()
consumer_secret = str(keys[1]).strip()

'''If we were doing a web app we might need a static call back but for this we can just use tweepy's standard'''
callback_uri = 'oob' # https://twitter.com

'''Get our authentication from twitter for our dev credentials'''
auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_uri)

'''Get a redirect URL from twitter so a user can autheticat their account for use'''
try:
    redirect_url = auth.get_authorization_url()
except tweepy.TweepError:
    print('Error! Failed to get request token.')

'''Open the redirect URL for authetication, user will get a Pin #'''
webbrowser.open(redirect_url)

'''Prompt the user to input the pin number twitter gave them after log in'''
user_pin = input("What is your twitter pin number? ")

'''Now we get the user token and user secret from twitter so we can access the account'''
auth.get_access_token(user_pin)

'''This gives us access to everything in the twitter API'''
api = tweepy.API(auth, wait_on_rate_limit=True)

'''
Part 1: A bank of key hashtags to look for and like up to 25 tweets at a go. If we cycle through more than 100
tweets before we like 25 we will break and move on to part 2
Part 2: Pull up to the three most recent tweets from @LXAI and like them
Part 3: Pull up to the three most recent tweets from @LXAI and rewteet them
'''
while True:
    search = '#ethicalai OR #aiethics OR #aiforsocialgood OR #ai4good OR #responsibleai OR #aijustice OR #dataforgood OR #data4good OR #aiforsocialimpact OR #futureofwork AND #AI'
    i = 0
    j = 0
    for tweet in tweepy.Cursor(api.search, search).items():
        try:
            tweet.favorite()
            i += 1
            print("Key hashtag tweet liked! Count: {}".format(i))
            time.sleep(3)
            if i >= 25:
                break
        except tweepy.TweepError as e:
            print(e.reason)
            j += 1
            if j > 100:
                break
            if '429' in str(e.reason):
                print("Sleeping 15 min for rate limit")
                time.sleep(960)
        except StopIteration:
            break
    alt_account1 = "_LXAI"
    i = 0
    j = 0
    for tweet in tweepy.Cursor(api.user_timeline, screen_name=alt_account1).items(5):
        try:
            tweet.favorite()
            i += 1
            print("{} tweet liked! Count: {}".format(alt_account1, i))
            if i >= 5:
                break
        except tweepy.TweepError as e:
            print(e.reason)
            j += 1
            if j >= 5:
                break
        except StopIteration:
            break
    user = api.get_user(alt_account1)
    user_timeline = user.timeline()
    for n in range(3):
        user_timeline_status_obj = user_timeline[n]
        status_obj_id = user_timeline_status_obj.id
        try:
            api.retweet(status_obj_id)
            print("Retweeted {} tweet {}!".format(alt_account1, status_obj_id))
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break
    time.sleep(900) 
