import requests

url = "http://127.0.0.1:8000/api/todos/"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM4NjYzNTczLCJpYXQiOjE3Mzg2NjMyNzMsImp0aSI6ImNlMjAxY2IxMmRmMTQ3YzZiOWFhOTZiMmUxN2Y1N2JiIiwidXNlcl9pZCI6MX0.1V04hqNmd4VYwWKUJuQZnqVfHYdwcin2s2Mk8bgCL5I"
}

response = requests.get(url, headers=headers)
print(response.json())