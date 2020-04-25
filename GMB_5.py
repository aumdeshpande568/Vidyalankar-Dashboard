import sys
import requests
import pandas as pd
from googleapiclient import sample_tools
import datetime

discovery_doc = "gmb_discovery.json"

temp_now = datetime.datetime.now() - datetime.timedelta(days=7)
now = (temp_now.strftime("%Y-%m-%d %H:%M:%S"))
#print(now)
#last_executed_date = "2020-03-15 00:00:00"

#FOR GETTING LOCAL SEARCH RANK
api_key = 'AIzaSyCPqrDh9jiMVtHn3MJaJ6hswspa7EdEpLY'
url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
verticals = ['mht cet','neet','iit jee','engineering','gate','bscit']
locations = ["andheri"]

def main(argv):
    # Use the discovery doc to build a service that we can use to make
    # MyBusiness API calls, and authenticate the user so we can access their
    # account
    service, flags = sample_tools.init(argv, "mybusiness", "v4", __doc__, __file__, scope="https://www.googleapis.com/auth/business.manage", discovery_filename=discovery_doc)

    # Get the list of accounts the authenticated user has access to
    output = service.accounts().list().execute()
    #print("List of Accounts:\n")
    #print(json.dumps(output, indent=2) + "\n")
    lid = "7760562933001019237"
    firstAccount = output["accounts"][0]["name"]
    body1 = {
        "locationNames": [
            ("accounts/108466677369484329492/locations/" + lid),
        ]
    }
    body2= {
        "parent":[
            ("accounts/108466677369484329492/locations/" + lid),
        ]
    }
    count=0
    # Get the list of locations for the first account in the list
    #print("List of Locations for Account " + firstAccount)
    locationsList = service.accounts().locations().list(parent=firstAccount).execute()
    locationsReviews = service.accounts().locations().reviews().list(parent="accounts/108466677369484329492/locations/7760562933001019237").execute()
    #print(json.dumps(locationsList, indent=2))
    l2 = locationsList
    l1 = locationsReviews
    print("Average Rating: "+ str(l1["averageRating"]))
    print("Total Reviews: " + str(l1["totalReviewCount"]))
    #print(l1["reviews"])
    temp=0
    n=0

    for row in locationsReviews.get('reviews'):
        review_date=(row['createTime'])
        temp_date = pd.to_datetime(review_date)
        converted_date = (temp_date.strftime("%Y-%m-%d %H:%M:%S"))

        if now<converted_date:
            n += 1

            if (row.get('starRating') == 'FIVE'):
                #print('5')
                temp += 5

            if (row.get('starRating') == 'FOUR'):
                #print('4')
                temp += 4

            if (row.get('starRating') == 'THREE'):
                #print('3')
                temp += 3

            if (row.get('starRating') == 'TWO'):
                #print('2')
                temp += 2

            if (row.get('starRating') == 'ONE'):
                #print('1')
                temp += 1

    final_rating = temp
    if n==0:
        print("No New Reviews")
    else:
        new_avg = final_rating/n
        fna = round(new_avg)
        print("Average Rating of New Reviews: "+str(fna))
        print("Average No. of New Weekly Reviews: " + str(n))

for i in range(len(verticals)):
    temp=0
    n=0
    for j in range(len(locations)):
        n += 1
        query = verticals[i]+" classes "+locations[j]
        #print(query)
        r = requests.get(url + 'query=' + query +'&key=' + api_key)
        x = r.json()
        y = x['results']
        count=0
        for k in range(len(y)):
            count+=1
            result = y[k]['name']
            #print(result)
            if result[:19] == "Vidyalankar Classes":
                #print(count)
                #print(verticals[i] +" "+locations[j] + " : " + str(count))
                break
        #print(count)
    print("Average Position of " + verticals[i].upper() + " for "+locations[0].upper()+": " + str(count))

if __name__ == "__main__":
    main(sys.argv)