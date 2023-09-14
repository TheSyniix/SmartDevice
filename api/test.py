import requests
url = 'http://localhost:3030/insert'
myobj = {
    "moisture":2.5,
    "time":2.5
}
x = requests.post(url, json = myobj)

