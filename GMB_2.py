import sys
import json
from googleapiclient.discovery import build
from googleapiclient import sample_tools
from googleapiclient.http import build_http
import pandas as pd
import datetime
import csv
from pandas.io.json import json_normalize

discovery_doc = "gmb_discovery.json"

def main(argv):
    # Use the discovery doc to build a service that we can use to make
    # MyBusiness API calls, and authenticate the user so we can access their
    # account
    service, flags = sample_tools.init(argv, "mybusiness", "v4", __doc__, __file__, scope="https://www.googleapis.com/auth/business.manage", discovery_filename=discovery_doc)
    # Get the list of accounts the authenticated user has access to
    output = service.accounts().list().execute()
    #print("List of Accounts:\n")


    firstAccount = output["accounts"][0]["name"]

    last_executed_date = "2020-04-8 00:00:00"
    form="https://bit.ly/2TJlPHr"
    overall = 0
    final_n = 0

    lids = ['7760562933001019237',"13110987815294434884","2134343411140012763", "17493438805552723046","2043349377754078974", "8575312462449434948","4463720830483140607","12014058896703999514","2564776461742891564","14119405071233287029","10004718908122045660","5308591117911507195","12736941806860522576","16971542478744721451","6847250793040778028","15742769480289306820","2131648888016274920","17001661978791282547","14479226342174298398", "3364090668868165727"]
    for i in lids:
        print(i)
        body = {
            "locationNames": [
                ("accounts/108466677369484329492/locations/"+i),
            ]
        }

        locationsReviews = service.accounts().locations().batchGetReviews(name=firstAccount, body=body).execute()
        locationsList = service.accounts().locations().list(parent=firstAccount).execute()
        l2 = locationsList
        print(l2["locations"][0]["locationName"])
        #print(json.dumps(locationsList, indent=2))
        cols_input= ['Review_ID','Display_Name','Rating']
        cols_output=['Rating', 'Comment']
        #print(locationsList['locationName'])
        df_input= pd.DataFrame(columns=cols_input)
        df_output=pd.DataFrame(columns=cols_output)
        temp = 0
        n = 0
        #count=0
        for row in locationsReviews.get('locationReviews'):
            row_temp_input = pd.DataFrame(columns=cols_input, index=range(1))
            row_temp_output = pd.DataFrame(columns=cols_output, index=range(1))
            row_temp_input['Review_ID'] = row.get('review').get('reviewId')
            row_temp_input['Rating'] = row.get('review').get('starRating')
            row_temp_output['Rating'] = row.get('review').get('starRating')
            row_temp_input['Display_Name'] = row.get('review').get('reviewer').get('displayName')
            reviewId = ("accounts/108466677369484329492/locations/"+i+"/reviews/"+row.get('review').get('reviewId'))
            positive = {
                "comment": ("Thank you for taking the time to share your positive feedback "+row.get('review').get('reviewer').get('displayName')+"! We are glad we could serve you well. :)")
            }
            negative = {
                "comment": ("Hi " + row.get('review').get('reviewer').get('displayName') + ", we are sorry to hear that feedback. For Vidyalankar, students come first and we would do whatever it takes to serve our students better. If you could fill this form regarding the inconvenience, it would help us fix the problem: "+form)
            }
            neutral = {
                "comment": ("Thank you for your feedback "+row.get('review').get('reviewer').get('displayName')+"!")
            }
            #count += 1
            review_date = row.get('review').get('updateTime')
            #print(review_date)
            temp_date = pd.to_datetime(review_date)
            converted_date = (temp_date.strftime("%Y-%m-%d %H:%M:%S"))

            #print(converted_date)

            if last_executed_date < converted_date:
                print("Replied to review")
                n +=1

                if (row.get('review').get('starRating') == 'FIVE'):
                    print('5')
                    response = service.accounts().locations().reviews().updateReply(name=reviewId, body=positive).execute()
                    print(response)
                    temp += 5

                if (row.get('review').get('starRating') == 'FOUR'):
                    print('4')
                    response = service.accounts().locations().reviews().updateReply(name=reviewId, body=positive).execute()
                    print(response)
                    temp +=4

                if(row.get('review').get('starRating') == 'THREE'):
                    print('3')
                    response = service.accounts().locations().reviews().updateReply(name=reviewId, body=neutral).execute()
                    print(response)
                    temp+=3

                if(row.get('review').get('starRating') == 'TWO'):
                    print('2')
                    response = service.accounts().locations().reviews().updateReply(name=reviewId, body=negative).execute()
                    print(response)
                    temp+=2

                if (row.get('review').get('starRating') == 'ONE'):
                    print('1')
                    response = service.accounts().locations().reviews().updateReply(name=reviewId, body=negative).execute()
                    print(response)
                    temp+=1

            else:
                print('Break')
                break
            #print(row_temp)
            #df_input = df_input.append(row_temp_input)
            #df_output = df_output.append(row_temp_output)
            if row.get('review').get('reviewReply') is None:
                aum = 0
            else:
                row_temp_output['Comment'] = row.get('review').get('reviewReply').get('comment')

    temp_now = datetime.datetime.now()
    now = (temp_now.strftime("%Y-%m-%d %H:%M:%S"))
    last_executed_date = now
    print("The program was successfully executed on:" + last_executed_date)


if __name__ == "__main__":
  main(sys.argv)
