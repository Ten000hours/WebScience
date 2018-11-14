import tweepy
import DBconnection
import utils


class StreamingApiForHashtag(tweepy.StreamListener):

    def on_status(self, status):
        # a = DBconnection.DBconnection('mongodb://localhost:27017/', "WEBSCIENCE", "twitter_meta_data")

        self.main(status)

    def on_error(self, status_code):
        if status_code == 420:
            return False

    def on_limit(self, track):
        print("limitation arrive")
        return False

    def main(self, status_main, **kwargs):
        # search by hashtag
        # for hashtag in status_main._json["entities"]["hashtags"]:
        #     print(hashtag)
        #     if hashtag["text"] == "MondayMotivation":
        print(status_main.text)

    # itemDicts = status_main._json
    # if len(kwargs) > 0:
    #     kwargs[0].insert_many_item(itemDicts)

    @classmethod
    def streamingSearchByHashtag(self, auth, instance, Hashtag):
        StreamingApiForHashtag = instance
        mystreaming = tweepy.Stream(auth=auth, listener=StreamingApiForHashtag)

        mystreaming.filter(track=[Hashtag], languages=["en"])


if __name__ == '__main__':
    # b = StreamingApiForHashtag()
    # StreamingApiForHashtag.streamingSearchByHashtag(b, "MondayMotivation")

    try:
        b = StreamingApiForHashtag()
        StreamingApiForHashtag.streamingSearchByHashtag(utils.api.auth, b, "#SundayMorning")
    except tweepy.RateLimitError:
        print("api hit the limit")
        try:
            SA = StreamingApiForHashtag()
            StreamingApiForHashtag.streamingSearchByHashtag(utils.api1.auth, SA, "#SundayMorning")
        except tweepy.RateLimitError:
            print("api1 hit the limit")
