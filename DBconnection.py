import pymongo
import StreamingApiForUser
import utils
from pymongo import MongoClient
from bson.son import SON
import matplotlib.pylab as plt

from datetime import datetime, timedelta
from dateutil.parser import parse


class DBconnection:
    dburl = ""
    dbText = ""
    collectionString = ""

    # url='mongodb://localhost:27017/'
    # dbText="WEBSCIENCE"
    # collectionString=  "twitter_meta_data"
    def __init__(self, url, dbText, *args):
        self.dburl = url
        self.dbText = dbText
        if len(args) > 0:
            self.collectionString = args[0]

    def dbconnect_to_collection(self):
        '''
        get the collection from database

        :return: collection
        '''
        try:
            myclient = pymongo.MongoClient(self.dburl)

            db = myclient[self.dbText]
            collection = db[self.collectionString]
            return collection
        except:
            print("fail to connect to collection(table)")

    def insert_one_item(self, itemDictOne):
        '''
        insert one data into collection
        :param itemDictOne: data (json)
        :return:
        '''
        x = self.dbconnect_to_collection().insert_one(itemDictOne)
        if x is not None:
            print("insert successfully")
        else:
            print("insert failed")

    def insert_many_item(self, itemDicts):
        '''
        insert many data into collection
        :param itemDicts: data (json)
        :return:
        '''
        x = self.dbconnect_to_collection().insert_one(itemDicts)
        # if x is not None:
        #     # print("insert many successfully")
        # else:
        #     print("insert many failed")

    @classmethod
    def count(cls,collection):
        '''
        get the number of data in collection
        :param collection:
        :return: the number of data
        '''
        count=0
        for elem in collection.find():
            count=count+1
        return count
    @classmethod
    def count_all(cls, collection):
        '''
        count the number of data and divide these data into time period
        :param collection:
        :return: list
                time
        '''
        list = []
        resultslist = []
        count = 0
        time = []
        # starttime = parse(elem["created_at"])
        for elem in collection.find():
            resultslist.append(elem)
        starttime = parse(resultslist[0]["created_at"])
        temp = starttime
        for elem in collection.find():
            nowtime = parse(elem["created_at"])
            if (nowtime - temp) < timedelta(minutes=10):
                count = count + 1
            elif (nowtime - temp) >= timedelta(minutes=10):
                list.append(count)
                count = 1
                temp = nowtime
                time.append(str(temp.strftime('%H:%M:%S')))

        return list, time

    @classmethod
    def count_all_google(cls, collection):
        '''
        count all function for google
        :param collection:
        :return:
        '''
        list = []
        resultslist = []
        count = 0
        time = []
        # starttime = parse(elem["created_at"])
        for elem in collection.find():
            resultslist.append(elem)
        starttime = parse(resultslist[0]["published"])
        temp = starttime
        for elem in collection.find():
            nowtime = parse(elem["published"])
            if -(nowtime - temp) < timedelta(minutes=10):
                count = count + 1
            elif -(nowtime - temp) >= timedelta(minutes=10):
                list.append(count)
                count = 1
                temp = nowtime
                time.append(str(temp.strftime('%H:%M:%S')))

        return list, time

    @classmethod
    def count_twitter_with_geotag(cls, collection):
        '''
        count the number of geotagged tweets and divide into time slice
        :param collection:
        :return: time list
        '''
        list = []
        resultslist = []
        count = 0
        time = []
        # starttime = parse(elem["created_at"])
        for elem in collection.find():
            resultslist.append(elem)
        starttime = parse(resultslist[0]["created_at"])
        temp = starttime
        for elem in collection.find():
            nowtime = parse(elem["created_at"])
            if elem["geo"] != None:
                for e in elem["geo"]:
                    if (e == "Glasgow" or "glasgow") and (nowtime - temp) < timedelta(minutes=10):
                        count = count + 1
                        break
                    elif e == "Glasgow" or "glasgow" and (nowtime - temp) >= timedelta(minutes=10):
                        list.append(count)
                        count = 1
                        temp = nowtime
                        time.append(str(temp.strftime('%H:%M:%S')))
                        break

        return list, time

    @classmethod
    def count_twitter_with_geotag_google(cls, collection):
        '''
        count geo for google plus
        :param collection:
        :return:
        '''
        list = []
        resultslist = []
        count = 0
        # time = []
        # starttime = parse(elem["created_at"])
        for elem in collection.find():
            resultslist.append(elem)
        starttime = parse(resultslist[0]["published"])
        temp = starttime
        for elem in collection.find():
            # nowtime = parse(elem["published"])
            if "location" in elem:
                for e in elem["location"].values():
                    if (e == "Glasgow" ):
                        count = count + 1



        return count

    @classmethod
    def count_retweet(cls, collection):
        '''
        count the retweet number in collection
        :param collection:
        :return:
        '''
        list = []
        resultslist = []
        count = 0
        time = []
        # starttime = parse(elem["created_at"])
        for elem in collection.find():
            resultslist.append(elem)
        starttime = parse(resultslist[0]["created_at"])
        temp = starttime
        for elem in collection.find():
            nowtime = parse(elem["created_at"])
            if elem["retweet_count"] == 0:
                continue
            elif elem["retweet_count"] != 0 and (nowtime - temp) < timedelta(minutes=10):
                count = count + 1
            elif elem["retweet_count"] != 0 and (nowtime - temp) >= timedelta(minutes=10):
                list.append(count)
                count = 1
                temp = nowtime
                time.append(str(temp.strftime('%H:%M:%S')))

        return list, time

    @classmethod
    def count_quotes(cls, collection):
        # count = 0
        # for elem in collection.find():
        #     if "quoted_status" in elem:
        #         if elem["quoted_status"] == None:
        #             continue
        #         else:
        #             count = count + 1
        #
        # return count
        list = []
        resultslist = []
        count = 0
        time = []

        for elem in collection.find():
            resultslist.append(elem)
        starttime = parse(resultslist[0]["created_at"])
        temp = starttime

        for elem in collection.find():
            nowtime = parse(elem["created_at"])
            if "quoted_status" in elem:
                if elem["quoted_status"] == None:
                    continue
                elif elem["quoted_status"] != None and (nowtime - temp) < timedelta(minutes=5):
                    count = count + 1

                elif elem["quoted_status"] != None and (nowtime - temp) >= timedelta(minutes=5):
                    list.append(count)
                    count = 1
                    temp = nowtime
                    time.append(str(temp.strftime('%H:%M:%S')))

        return list, time

    @classmethod
    def redundant_tweets_count(cls, collec1, collec2):
        '''
        count redundent tweets from two different collections
        :param collec1: string
        :param collec2: string
        :return: print out the same tweets
        '''
        collection1 = collec1
        collection2 = collec2
        db = MongoClient().WEBSCIENCE
        pipeline = [
            {"$unwind": "$text"},
            {"$group": {"_id": "$text", "count": {"$sum": 1}}},
            {"$sort": SON([("count", -1), ("_id", -1)])}
        ]
        if collection1 == "twitter_REST_search_geo":
            a = list(db.twitter_REST_search_geo.aggregate(pipeline))
        if collection1 == "Twitter_location_with_tag":
            a = list(db.Twitter_location_with_tag.aggregate(pipeline))
        if collection1 == "Twitter_location_without_tag":
            a = list(db.Twitter_location_without_tag.aggregate(pipeline))
        if collection2 == "twitter_REST_search_geo":
            b = list(db.twitter_REST_search_geo.aggregate(pipeline))
        if collection2 == "Twitter_location_with_tag":
            b = list(db.Twitter_location_with_tag.aggregate(pipeline))
        if collection2 == "Twitter_location_without_tag":
            b = list(db.Twitter_location_without_tag.aggregate(pipeline))

        for Aelem in a:
            for belem in b:
                if Aelem["_id"] == belem["_id"]:
                    print(belem)


if __name__ == '__main__':
    a = DBconnection('mongodb://localhost:27017/', "WEBSCIENCE", "twitter_REST_search_geo")
    # # for elem in a.dbconnect_to_collection().find():
    # #     print(elem)
    # print(DBconnection.count_twitter_with_geotag(a.dbconnect_to_collection()))
    # for elemt in a.dbconnect_to_collection().find():
    #     print(elemt["geo"])
    # print(DBconnection.count_twitter_with_geotag(a.dbconnect_to_collection()))

    list, time = DBconnection.count_quotes(a.dbconnect_to_collection())
    plt.bar(range(len(list)), list)
    plt.xticks(range(len(time)), time)
    plt.savefig("countquote.pdf")
    plt.show()
    # DBconnection.redundant_tweets_count("Twitter_location_without_tag", "Twitter_location_with_tag")
    # mystreaming = tweepy.Stream(auth=utils.api.auth, listener=api)
    # mystreaming.filter(track=['glasgow'],locations=[-85.966087,36.956463,-85.871681,37.04779])
