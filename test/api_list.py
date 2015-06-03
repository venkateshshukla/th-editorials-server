import json
import requests
from datetime import datetime

def print_r(d, n=0):
	if isinstance(d, dict):
		for i in d:
			print '\t' * n, i,':',
			print_r(d[i])
	elif isinstance(d, list):
		for i in d:
			print ''
			print_r(i, n + 1)
	else:
		print d

url = 'http://localhost:8080/api/list'
now = datetime(2015, 6, 3)
timestamp = (now - datetime(1970, 1, 1)).total_seconds()

data = {}
data['timestamp'] = timestamp

r = requests.post(url, params=data)
print r.status_code

j = json.loads(r.content)
print_r(j)
