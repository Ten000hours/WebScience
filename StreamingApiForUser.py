import tweepy
import DBconnection
import utils


class StreamingApiForUser(tweepy.StreamListener):

    def on_status(self, status):
        # a = DBconnection.DBconnection('mongodb://localhost:27017/', "WEBSCIENCE", "twitter_meta_data")

        self.main(status)

    def on_error(self, status_code):
        print(status_code)

    def on_limit(self, track):
        print("limitation arrive")
        return False

    def main(self, status_main, **kwargs):
        # search by userid
        print(status_main._json)

        # itemDicts = status_main._json
        # if len(kwargs) > 0:
        #     kwargs[0].insert_many_item(itemDicts)

    @classmethod
    def streamingSearchByUserID(self, instance, userID):
        StreamingApiForUser = instance
        mystreaming = tweepy.Stream(auth=utils.api1.auth, listener=StreamingApiForUser)

        mystreaming.filter(follow=[userID], async=True, languages="en")


if __name__ == '__main__':
    b = StreamingApiForUser()
    StreamingApiForUser.streamingSearchByUserID(b, "25073877")
