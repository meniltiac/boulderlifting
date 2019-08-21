#!/usr/bin/env python3
from woocommerce import API
import sys

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

def main(args=None):
    page = 0    
    accounts = {}

    while(1):
        page += 1
        subscribers = wcapi.get("subscriptions?page="+str(page)).json()
        if len(subscribers) == 0:
            break
        for subscriber in subscribers:
            if not subscriber["status"] in accounts:
                accounts[subscriber["status"]] = []
            accounts[subscriber["status"]].append(subscriber["billing"]["email"])
    print("\n%d pages" % (page))
    
    for account_status in accounts.keys():
        print("\n%s (%d):" % (account_status, len(accounts[account_status])))
        print(', '.join(accounts[account_status]))

if __name__ == "__main__":
    main()
