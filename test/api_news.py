import logging
import requests
import json

from api_list import post_list, print_r

localhost = 'http://localhost:8080/api/news'

def post_news(key, url=localhost):
	logging.debug('key = {}'.format(key))
	data = {}
	data['key'] = key
	r = requests.post(url, params=data)
	logging.debug('response code : {}'.format(r.status_code))
	return json.loads(r.content)


resp = post_list()
entries = resp['entries']
for e in entries:
	key = e['key']
	j = post_news(key)
	print ''
	print_r(j)
