# WebScience
This is the implementation of Twitter data crawler and its data analyse code.
Using TF-IDF and LSH(locality sensitive Hashing) to group tweets and assign geo-tags
to those non-geotagged tweets.

University of Glasgow Course Web Science CourseWork

The result of grouping tweets:
https://github.com/Ten000hours/WebScience/blob/master/TwitterCluster.pdf

## requirements
###
    tweepy
    pymongo
    bson.son
    matplotlib.pylab
    datetime
    dateutil.parser
    google-api-python-client
    httplib2
    regex
    sklearn.feature_extraction.text
    nltk.corpus

Note that you may need to download corresponding lib of nltk,so before running the script
running following code to download
###
     nltk.download("corpus")
     nltk.download("stopwords")
You also need to install MongoDB in advance and change the directory path in the code .