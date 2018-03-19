#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import sys


#Twitter API credentials

consumer_key = "INSERT CONSUMER KEY"
consumer_secret = "INSERT CONSUMER SECRET"
access_key = "INSERT ACCESS KEY"
access_secret = "INSERT ACCESS SECRET"


def get_all_tweets(name):

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)


    replies=[] 
    non_bmp_map = dict.fromkeys(range(0x10000, 65536), 0xfffd)  
    for full_tweets in tweepy.Cursor(api.user_timeline,screen_name=name,timeout=999999).items(10):
      for tweet in tweepy.Cursor(api.search,q='to:'+name,result_type='recent',timeout=999999).items(1000):
        if hasattr(tweet, 'in_reply_to_status_id_str'):
          if (tweet.in_reply_to_status_id_str==full_tweets.id_str):
            replies.append(tweet.text)
      print("Tweet :",full_tweets.text.translate(non_bmp_map))
      for elements in replies:
           print("Replies :",elements)
    replies = []
    

if __name__ == '__main__':

    get_all_tweets("aditigupta1709")
