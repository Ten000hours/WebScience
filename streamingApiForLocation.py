import tweepy
import DBconnection
import utils
import pymongo


class StreamingApiForLocation(tweepy.StreamListener):

    def on_status(self, status):
        a = DBconnection.DBconnection('mongodb://localhost:27017/', "WEBSCIENCE", "Twitter_location_with_tag")
        b = DBconnection.DBconnection(
            'mongodb://localhost:27017/', "WEBSCIENCE", "Twitter_location_without_tag")
        self.main(status, a, b)

    def on_error(self, status_code):
        if status_code == 420:
            return False

    def on_limit(self, track):
        print("limitation arrive")
        return False

    def main(self, status_main, instance1, instance2):
        # print(status_main._json)
        if status_main._json["geo"] != None:
            for elem in status_main._json["geo"]:
                if elem == "glasgow" or "Glasgow":
                    print(status_main._json)
                    itemDicts = status_main._json
                    try:
                        instance1.insert_many_item(itemDicts)
                    except pymongo.errors.DuplicateKeyError:
                        continue
        else:
            print(status_main._json)
            itemDicts = status_main._json

            try:
                instance2.insert_many_item(itemDicts)
            except pymongo.errors.DuplicateKeyError:
                print("duplicate")

        # itemDicts = status_main._json
        # if len(kwargs) > 0:
        #     kwargs[0].insert_many_item(itemDicts)

    @classmethod
    def streamingSearchByGeo(self, instance, Location):
        StreamingApiForUser = instance
        mystreaming = tweepy.Stream(auth=utils.api.auth, listener=StreamingApiForUser)
        mystreaming.filter(locations=Location, languages=["en"])


if __name__ == '__main__':
    b = StreamingApiForLocation()
    StreamingApiForLocation.streamingSearchByGeo(b, [-4.6186, 55.7215, -3.8678, 55.9898])
