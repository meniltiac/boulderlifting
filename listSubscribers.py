#!/usr/bin/env python3
from woocommerce import API

# Replace consumer_key and consumer_secret before running - it can be found
# in the email chain entitled "Python script to list subscribers"
wcapi = API(
    url="https://boulderlifting.com",
    consumer_key="XXXXXXXXXXX",
    consumer_secret="XXXXXXXXXXX",
    wp_api=True,
    version="wc/v1",
    query_string_auth=True
)

page = 0
while(1):
    page += 1
    subscribers = wcapi.get("subscriptions?page="+str(page)).json()
    if len(subscribers) == 0:
        print("\n\nNo more subscribers on page " + str(page))
        break
    for subscriber in subscribers:
        if(subscriber["status"] == "active"):
            print(subscriber["billing"]["email"], end=', ')
