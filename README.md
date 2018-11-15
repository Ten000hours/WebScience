# WebScience
This is the implementation of Twitter data crawler and its data analyse code.
Using TF-IDF and LSH(locality sensitive Hashing) to group tweets and assign geo-tags
to those non-geotagged tweets.

University of Glasgow Course Web Science CourseWork

The result of grouping tweets:
https://github.com/Ten000hours/WebScience/blob/master/TwitterCluster.pdf

We also analysed another platform----Google Plus using the same method and the result of
grouping data:
https://github.com/Ten000hours/WebScience/blob/master/GoogleCluster.pdf
## requirements
Using "pip install --" command to install following libs:
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
     import nltk

     nltk.download("corpus")
     nltk.download("stopwords")
You also need to install MongoDB in advance and change the directory path in the code .

## Data import
Before running the python code,you need to import the json data (data.rar) into MongoDB using following code in command prompt:


###
    mongoimport -d WEBSCIENCE -c Twitter_REST_search_geo --file Twitter_REST_search_geo.json --type json
    mongoimport -d WEBSCIENCE -c Twitter_location_without_tag --file Twitter_location_without_tag.json --type json
    mongoimport -d WEBSCIENCE -c Twitter_location_with_tag --file Twitter_location_with_tag.json --type json
    mongoimport -d WEBSCIENCE -c GooglePlus_text_glasgow --file GooglePlus_text_glasgow.json --type json

## Citaion
This project applied following code :
###
     LSH python version: https://github.com/totalgood/LSHash