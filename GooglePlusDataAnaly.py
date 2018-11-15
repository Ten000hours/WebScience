import DBconnection
import regex as re
from sklearn.feature_extraction.text import CountVectorizer
from lshash.lshash import LSHash
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.corpus import stopwords
import nltk
import numpy as np
from matplotlib import pyplot as plt

# nltk.download("corpus")
# nltk.download("stopwords")
a = DBconnection.DBconnection('mongodb://localhost:27017/', "WEBSCIENCE", "GooglePlus_text_glasgow")

words = set(nltk.corpus.words.words())


#
corpus = []
for elemt in a.dbconnect_to_collection().find():

    text = re.sub('[^A-Za-z]+', ' ', elemt["title"])
    textlist = nltk.word_tokenize(text)

    text1 = " ".join(w for w in textlist \
                     if w.lower() in words or not w.isalpha())
    textlist = nltk.word_tokenize(text1)

    for word in textlist:  # iterate over word_list
        if word in stopwords.words('english'):
            textlist.remove(word)
    final = " ".join(w for w in textlist)

    # text = re.sub(r'@\S+|https?://\S+', '', elemt["text"])
    corpus.append(final)

#  convert the words into word frequency matrix
vectorizer1 = CountVectorizer()

X = vectorizer1.fit_transform(corpus)
# get the keywords in corpus
word = vectorizer1.get_feature_names()


transformer = TfidfTransformer()

#  calculate the TF-IDF values
tfidf = transformer.fit_transform(X)



# print(tfidf)

lsh = LSHash(6, 8)

# seperate the geo-tagged data into two list
locatList = []
noneList = []
for elemts in a.dbconnect_to_collection().find():
    if "location" in elemts:
        for e in elemts["location"].values():
            if e == "Glasgow":
                locatList.append(elemts)
    else:
        noneList.append(elemts)
# construct the centriodSet
centriodSet = []
Ind = 0
for i in range(0, len(locatList)):
    centriod = []
    j = 0
    while j < (tfidf.indptr[i + 1] - tfidf.indptr[i]):
        if j > 7:
            break
        centriod.append(round(tfidf.data[Ind + j], 2))
        j += 1
    if len(centriod) < 8:
        for index in range(8 - len(centriod)):
            centriod.append(0 + 1)
    lsh.index(centriod)
    Ind += tfidf.indptr[i + 1] - tfidf.indptr[i]
    # if len(centriod)!=11:
    #     print(len(centriod),i)
    centriodSet.append(centriod)

# construct the noneList which contains non-geo data
count = np.zeros(len(locatList))

index2 = tfidf.indptr[len(locatList)]
for i in range(0,
               len(noneList)):
    b = []
    j = 0
    while j < (tfidf.indptr[i + 1] - tfidf.indptr[i]):
        if j > 7:
            break
        b.append(round(tfidf.data[index2 + j], 2))
        j += 1
    if len(b) < 8:
        for index in range(8 - len(b)):
            b.append(1)
    fianlresu = lsh.query(b)
    whileflag = 0
    while not fianlresu and whileflag < 3:
        fianlresu = lsh.query(b)
        whileflag += 1

    if not fianlresu:
        count[0] += 1
        # print(assinglist[i])

    else:
        checklist = []
        for elem in fianlresu[0][0]:
            checklist.append(elem)
        count[centriodSet.index(checklist)] += 1

    index2 += tfidf.indptr[i + 1] - tfidf.indptr[i]
# printout the result
print(count)
print(sum(count))

plt.bar(range(len(locatList)), count, color=["red", "green", "blue"])
plt.title("Google Cluster")
plt.savefig("GoogleCluster.pdf", bbox="tight")
plt.show()

