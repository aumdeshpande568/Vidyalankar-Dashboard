
# importing required modules
import requests, json
import time

# enter your api key here
api_key = 'YOUR_API_KEY'

# url variable store url
url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

verticals = ['mht cet','neet','iit jee','engineering','gate','bscit']
locations = ['mumbai','dadar','chembur','thane','dombivli','panvel','andheri','borivali','kandivli','kalyan','pune','vashi','nerul']


n=0

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
                print(verticals[i] +" "+locations[j] + " : " + str(count))
                break
        #print(count)
        temp += count
    position = temp / n
    final_position = round(position)
    print("Average Position for " + verticals[i].upper() + " : " + str(final_position))
