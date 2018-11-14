import httplib2
import apiclient.discovery  # pip install google-api-python-client
from DBconnection import *
import time
from matplotlib import pyplot as plt

service = apiclient.discovery.build('plus', 'v1', http=httplib2.Http(),
                                    developerKey="AIzaSyCeoTt0szZDhNRiImSP93uuqt94dKe1ikA")
activities_resource = service.activities()
request = activities_resource.search(
    query="glasgow",
    maxResults='20')
start = time.time()
analytic = []
count = 0
b = DBconnection(
    'mongodb://localhost:27017/', "WEBSCIENCE", "GooglePlus_text_glasgow")
temp=start
while request != None:
    end = time.time()

    if int(end - temp) == 5 * 60:
        analytic.append(count)
        print("===========", analytic)
        count=0
        temp=end
    if int(end - start) == 30 * 60:
        break
    try:
        activities_document = request.execute()
    except:
        print("error")
        continue
    if 'items' in activities_document:
        print('got page with %d' % len(activities_document['items']))
        count += len(activities_document['items'])

        for activity in activities_document['items']:
            # print (activity['id'], activity['object']['content'])
            # print(activity)
            b.insert_many_item(activity)

    request = service.activities().search_next(request, activities_document)

print(analytic)
plt.bar(range(len(analytic)), analytic)
plt.title("How many activities will recevice per 5mins")
plt.savefig("datacrawlfromGooglePlus.pdf", bbox="tight")
plt.show()
