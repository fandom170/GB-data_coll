import json
import requests

with open('credentials_hw_2-01.csv', 'r') as f:
    creds = f.read().split(',')
    main_url = creds[0].lstrip()
    username = creds[1]
    password = creds[2]
    profile = creds[3]
    domain = creds[4]
    assig_id = creds[5]
    URI = creds[6]

locale = 'EN_US'
timezone = 'GMT'
dateFormat = '3'
timeFormat = '3'

endpoint = "domains/{}/logon".format(domain)

headers = {"Content-Type": "application/json",
           "User-Agent": "python-requests/2.25.1"
           }

data = json.dumps({
    'username': username,
    'password': password,
    'profile': profile,
    'locale': locale,
    'timezone': timezone,
    'dateFormat': dateFormat,
    'timeFormat': timeFormat
}, indent=4)

url = main_url + endpoint
logon = requests.post(url=url, data=data, headers = headers)

session_id = logon.json()['SID']

#get some data from system
endpoint = f"v1/{URI}/{assig_id}"
headers = {"Content-Type": "application/json",
           "User-Agent": "python-requests/2.25.1",
           "x-adapt-sid": session_id}

url = main_url + endpoint
get_data = requests.get(url=url, headers=headers)

result = json.dumps(get_data.json(), indent=4)

with open('result_hw_2-01.json', 'w') as fw:
    fw.write(result)
