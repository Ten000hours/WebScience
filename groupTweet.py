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
a = DBconnection.DBconnection('mongodb://localhost:27017/', "WEBSCIENCE", "Twitter_location_with_tag")
b = DBconnection.DBconnection('mongodb://localhost:27017/', "WEBSCIENCE", "Twitter_location_without_tag")

words = set(nltk.corpus.words.words())

geolist = []
for element in a.dbconnect_to_collection().find():
    geolist.append(element["geo"])

assinglist = []
for elemet in b.dbconnect_to_collection().find():
    assinglist.append(elemet["text"])
# print(geolist[0])
# 语料
corpus = []
for elemt in a.dbconnect_to_collection().find():
    text = re.sub('[^A-Za-z]+', ' ', elemt["text"])
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
    # print(text)

for elemt in b.dbconnect_to_collection().find():
    text = re.sub('[^A-Za-z]+', ' ', elemt["text"])
    textlist = nltk.word_tokenize(text)

    text1 = " ".join(w for w in textlist \
                     if w.lower() in words or not w.isalpha())
    textlist = nltk.word_tokenize(text1)

    for word in textlist:  # iterate over word_list
        if word in stopwords.words('english'):
            textlist.remove(word)
    final = " ".join(w for w in textlist)

    corpus.append(text)
    # print(text)
# 将文本中的词语转换为词频矩阵
vectorizer1 = CountVectorizer()

X = vectorizer1.fit_transform(corpus)
# 获取词袋中所有文本关键词
word = vectorizer1.get_feature_names()
# print(word)
# 查看词频结果
# print(X.toarray())

transformer = TfidfTransformer()

# 将词频矩阵X统计成TF-IDF值
tfidf = transformer.fit_transform(X)

# 查看数据结构 tfidf[i][j]表示i类文本中的tf-idf权重
list = tfidf
# print(tfidf)

lsh = LSHash(6, 8)
# len(tfidf.todense()[0]
# for i in range(82):
#     a = list()
#     for j in range(11):
#         # print(tfidf.toarray()[i][j])
#         a.append(tfidf.toarray()[i][j])
#     # print(a)
#     lsh.index(a)
centriodSet = []
Ind = 0
for i in range(0, 82 - 1):
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
# print(centriodSet)

count = np.zeros(82)

index2 = tfidf.indptr[82]
for i in range(82, DBconnection.DBconnection.count_all(b.dbconnect_to_collection()) - 1):
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
        print(assinglist[i])

    else:
        checklist = []
        for elem in fianlresu[0][0]:
            checklist.append(elem)
        count[centriodSet.index(checklist)] += 1

        assinglist[i] = assinglist[i] + " " + str(geolist[centriodSet.index(checklist)])
        # .append(geolist[centriodSet.index(checklist)])
        print(assinglist[i])

    index2 += tfidf.indptr[i + 1] - tfidf.indptr[i]

print(count)
print(sum(count))

plt.bar(range(82), count, color=["red", "green", "blue"])
plt.title("Tweets Cluster")
plt.savefig("TwitterCluster.pdf",bbox="tight")
plt.show()
# for j in range(11, 22):
#     # print(tfidf.toarray()[9][j])
#     b.append(tfidf.toarray()[110][j])
#     print(b)
# print(b)

# checklist = []
# for elem in fianlresu:
#     checklist.append(elem)
# print(geolist[centriodSet.index(checklist)])
