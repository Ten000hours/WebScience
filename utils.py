# 导入tweepy
import tweepy
import time
import DBconnection
import pymongo

# write twitter app Key and secret
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
# webscienceThread1
consumer_key1 = ''
consumer_secret1 = ''
access_token1 = ''
access_token_secret1 = ''
# webscienceThread2
consumer_key2 = ''
consumer_secret2 = ''
access_token2 = ''
access_token_secret2 = ''
# webscienceThread3
consumer_key3 = ''
consumer_secret3 = ''
access_token3 = ''
access_token_secret3 = ''
#authenticate the app
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

auth1 = tweepy.OAuthHandler(consumer_key1, consumer_secret1)
auth1.set_access_token(access_token1, access_token_secret1)

auth2 = tweepy.OAuthHandler(consumer_key2, consumer_secret2)
auth2.set_access_token(access_token2, access_token_secret2)

auth3 = tweepy.OAuthHandler(consumer_key3, consumer_secret3)
auth3.set_access_token(access_token3, access_token_secret3)
# get the api
api = tweepy.API(auth)

api1 = tweepy.API(auth1)

api2 = tweepy.API(auth2)

api3 = tweepy.API(auth3)


def search():
    return api.search('Glasgow', lang="en")


def search1():
    return api1.search("Glasgow", lang="en")


def search2():
    return api2.search("Glasgow", lang="en")


def search3():
    return api3.search("Glasgow", lang="en")


def dataCrawler():
    a = DBconnection.DBconnection('mongodb://localhost:27017/', "WEBSCIENCE", "twitter_REST_search_geo")
    while 1:
        while 1:
            try:
                # thread1
                resultset = search()
                for result in resultset:
                    itemDicts = result._json
                    try:
                        a.insert_many_item(itemDicts)
                        print(result._json)
                    except pymongo.errors.DuplicateKeyError:
                        continue
            except tweepy.RateLimitError:
                print("api hit the limit")
                time.sleep(60 * 1)
                break

        while 1:
            try:
                # theard2
                resultset1 = search1()
                for result1 in resultset1:
                    itemDicts1 = result1._json
                    try:
                        a.insert_many_item(itemDicts1)
                        print(result1._json)
                    except pymongo.errors.DuplicateKeyError:
                        continue
            except tweepy.RateLimitError:
                print("api1 hit the limit")
                time.sleep(60 * 1)
                break

        while 1:
            try:
                # thread3
                resultset2 = search2()
                for result2 in resultset2:
                    itemDicts2 = result2._json
                    try:
                        a.insert_many_item(itemDicts2)
                        print(result2._json)
                    except pymongo.errors.DuplicateKeyError:
                        continue
            except tweepy.RateLimitError:
                print("api2 hit the limit")
                time.sleep(60 * 1)
                break

        while 1:
            try:
                # theard4
                resultset3 = search3()
                for result3 in resultset3:
                    itemDicts3 = result3._json
                    try:
                        a.insert_many_item(itemDicts3)
                        print(result3._json)
                    except pymongo.errors.DuplicateKeyError:
                        continue
            except tweepy.RateLimitError:
                print("api3 hit the limit")
                time.sleep(60 * 1)
                break
        time.sleep(60 * 8)


if __name__ == '__main__':
    dataCrawler()
