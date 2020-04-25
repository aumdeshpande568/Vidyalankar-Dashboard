import json
import sys

from googleapiclient import sample_tools


discovery_doc = "gmb_discovery.json"

def main(argv):
    # Use the discovery doc to build a service that we can use to make
    # MyBusiness API calls, and authenticate the user so we can access their
    # account
    service, flags = sample_tools.init(argv, "mybusiness", "v4", __doc__, __file__, scope="https://www.googleapis.com/auth/business.manage", discovery_filename=discovery_doc)
    # Get the list of accounts the authenticated user has access to
    output = service.accounts().list().execute()


    firstAccount = output["accounts"][0]["name"]

#TAKE VALUE OF LAST EXECUTED DATE FROM DB
    last_executed_date="2020-02-15 10:48:55"
    lid="7760562933001019237"

    body = {
            "locationNames": [
                "accounts/108466677369484329492/locations/7760562933001019237"
            ],
            "basicRequest": {
                "metricRequests": [
                    {
                        "metric": "QUERIES_DIRECT"
                    },
                    {
                        "metric": "QUERIES_INDIRECT"
                    },
                    {
                        "metric": "QUERIES_CHAIN"
                    },
                    {
                        "metric": "ACTIONS_WEBSITE"
                    },
                    {
                        "metric": "ACTIONS_PHONE"
                    },
                    {
                        "metric": "VIEWS_SEARCH"
                    },
                ],
                "timeRange": {
                    "startTime":
                        "2020-04-02T00:00:00Z",
                    "endTime":
                        "2020-04-09T00:00:00Z"
                }
            }
        }
    locationsList = service.accounts().locations().list(parent=firstAccount).execute()
    l2 = locationsList
    #print(l2["locations"][0]["locationName"])
    locationInsights = service.accounts().locations().reportInsights(name=firstAccount, body=body).execute()
    #print(json.dumps(locationInsights,indent = 2) +"\n")
    metricValList= locationInsights['locationMetrics'][0]['metricValues']
    queriesIndirect=0
    queriesChain=0
    for valObject in metricValList:
        print('Metric: ' + valObject['metric'] + '\tValue: ' + valObject['totalValue']['value'])
        if( valObject['metric'] == 'QUERIES_CHAIN'):
            queriesChain = int(valObject['totalValue']['value'])
        if (valObject['metric'] == 'QUERIES_INDIRECT'):
            queriesIndirect = int(valObject['totalValue']['value'])
    print('QUERIES CATEGORY : '+str(queriesIndirect - queriesChain ))

if __name__ == "__main__":
  main(sys.argv)