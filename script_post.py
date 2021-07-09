import requests

url = 'http://localhost:8000/post/'
data = {'teste': 'teste'}

resp = requests.post(url, data=data)

print(resp.status_code)
print(resp.text)