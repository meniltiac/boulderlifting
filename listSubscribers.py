#!/usr/bin/env python3
from woocommerce import API
import sys

# read secrets from a file, so they aren't committed to git repo.
# two values are needed, consumer_key and consumer_secret.
secrets = {}
with open('wordpress_secrets.json') as file:
    exec(file.read(), secrets)

# Replace consumer_key and consumer_secret before running - it can be found
# in the email chain entitled "Python script to list subscribers"
wcapi = API(
    url="https://boulderlifting.com",
    consumer_key=secrets['consumer_key'],
    consumer_secret=secrets['consumer_secret'],
    wp_api=True,
    version="wc/v1",
    query_string_auth=True
)

def print_list(title, l):
    print("\n%s (%d):" % (title, len(l)))
    print("---------------------------------------------------------------------------------------")
    print(', '.join(l))

def main(args=None):
    page = 0    
    accounts = {}
    total_income = 0.0
    members = 0

    while(1):
        page += 1
        subscribers = wcapi.get("subscriptions?page="+str(page)).json()
        print('.', end='', flush=True)
        if len(subscribers) == 0:
            break
        for subscriber in subscribers:
            if not subscriber["status"] in accounts:
                accounts[subscriber["status"]] = []
            accounts[subscriber["status"]].append(subscriber["billing"]["email"])
            if subscriber["status"] == 'active':
                #print(subscriber['line_items'])
                for li in subscriber['line_items']:
                    price = float(li["total"])
                    if price > 0.01:
                        total_income += price
                        members += int(li["quantity"])
    print(" %d pages" % (page))
    print("%d paid memberships, $%.2f / month ($%.0f/member)" % (members, total_income, total_income/members))
    
    for account_status in accounts.keys():
        acct_list = accounts[account_status]
        # remove duplicates that are also in the 'active' list.
        # these duplicates occur when somoene canceled but signed up again
        dups = []
        if account_status != 'active':
            for a in acct_list:
                if a in accounts['active']:
                    acct_list.remove(a)
                    dups.append(a)
            if len(dups) > 0:
                print_list(account_status + ' DUPLICATES', dups)
            
        print_list(account_status, acct_list)

if __name__ == "__main__":
    main()
