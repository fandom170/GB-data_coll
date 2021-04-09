import requests

#login = None
#password = None

with open('credentials.csv', 'r')as f:
    creds = f.readline().split(',')
    login = creds[0]
    password = creds[1]

print(password)

url = "http://www.google.com"

headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                    'Authorization':'Basic cG9zdG1hbjpwYXNzd29yZA=='}


init_request = requests.get(url, headers = headers)

#print(init_request)
#print(init_request.headers)



