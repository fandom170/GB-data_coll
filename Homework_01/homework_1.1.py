import requests
import json


with open('credentials.csv', 'r')as f:
    creds = f.readline().split(',')
    login = creds[0]
    password = creds[1]
    token = creds[2]

main_url = 'https://api.github.com'
area = '/users'
endpoint = '/repos'
personal = '/' + login


headers_request = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 OPR/75.0.3969.149',
                  'Accept': 'application/vnd.github.v3+json'}


url = main_url + area + personal + endpoint
repos_response = requests.get(url, headers_request)
#print(repos_response.json())

with open('result_hw1.json', 'w')as fw:
    fw.write(json.dumps(repos_response.json(), indent=4))
