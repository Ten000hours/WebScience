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

## Data import
Before running the python code,you need to import the json data using following code in command prompt:

###
    mongoimport -d WEBSCIENCE -c Twitter_REST_search_geo --file Twitter_REST_search_geo.json --type json
    mongoimport -d WEBSCIENCE -c Twitter_location_without_tag --file Twitter_location_without_tag.json --type json
    mongoimport -d WEBSCIENCE -c Twitter_location_with_tag --file Twitter_location_with_tag.json --type json
    mongoimport -d WEBSCIENCE -c GooglePlus_text_glasgow --file GooglePlus_text_glasgow.json --type json
