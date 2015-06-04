import sys
import json
import requests
import logging
from datetime import datetime, timedelta

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

localhost = 'http://localhost:8080/api/list'
def post_list(url=localhost, date=(datetime.now()-timedelta(days=1))):
	logging.debug('URL : {}'.format(url))
	logging.debug('Starting date : {}'.format(date))
	timestamp = (date - datetime(1970, 1, 1)).total_seconds()

	data = {}
	data['timestamp'] = timestamp

	r = requests.post(url, params=data)
	logging.debug('Response status : {}'.format(r.status_code))

	j = json.loads(r.content)
	return j

if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG)
	if len(sys.argv) == 2:
		url = sys.argv[1]
	else:
		url = localhost
	today = (datetime.now() - timedelta(days=1)).replace(hour=0, minute=0,
			second=0)
	j = post_list(url, today)
	print_r(j)
