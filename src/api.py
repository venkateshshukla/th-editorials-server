import json
import logging

from datetime import datetime
from webapp2 import RequestHandler, WSGIApplication

from auth import Auth
from errors import AuthError, InvalidRequestError
from extract import Extract
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
			kind, link = Opinion.getKindLink(ky)
			logging.debug('kind for given key : {}'.format(kind))
			logging.debug('Link for given key : {}'.format(link))
			snp = Extract.getHtmLsNIPPET(kind, link)
			self.response.content_type='application/json'
			data = {}
			data['snippet'] = snp
			data['key'] = ky
			data['kind'] = kind
			self.response.write(json.dumps(data))

		except AuthError:
			logging.exception('AuthError')
			self.response.set_status(403)
		except InvalidRequestError:
			logging.exception('InvalidRequestError')
			self.response.set_status(400)

app = WSGIApplication([ ('/api/list', List), ('/api/news', News)], debug=True)
