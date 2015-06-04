import logging
import json

from datetime import datetime
from webapp2 import RequestHandler, WSGIApplication

from auth import Auth
from errors import AuthError, InvalidRequestError
from opinion import Opinion

class List(RequestHandler):
	def check_valid(self):
		pass

	def post(self):
		try:
			Auth.check_auth(self.request.headers)
			self.check_valid()
			ts = float(self.request.get('timestamp'))
			logging.debug("Received timestamp : {}".format(ts))
			ls = Opinion.getJsonListStarting(ts)
			self.response.content_type='application/json'
			self.response.write(ls)

		except AuthError:
			logging.exception('AuthError')
			self.response.set_status(403)
		except InvalidRequestError:
			logging.exception('InvalidRequestError')
			self.response.set_status(400)

class News(RequestHandler):
	def check_valid(self):
		pass

	def post(self):
		try:
			Auth.check_auth(self.request.headers)
			self.check_valid()

			ky = self.request.get('key')
			logging.debug('Recieved key : {}'.format(ky))
			kind, url = Opinion.getKindUrl(ky)
			logging.debug('kind for given key : {}'.format(kind))
			logging.debug('Url for given key : {}'.format(url))
			self.response.content_type='application/json'
			self.response.write(json.dumps({'url' : url, 'key' :
				key, 'kind' : kind}))

		except AuthError:
			logging.exception('AuthError')
			self.response.set_status(403)
		except InvalidRequestError:
			logging.exception('InvalidRequestError')
			self.response.set_status(400)

app = WSGIApplication([ ('/api/list', List), ('/api/news', News)], debug=True)
