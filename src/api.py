import json
import logging

from datetime import datetime
from webapp2 import RequestHandler, WSGIApplication

from auth import Auth
from constants import Kind
from errors import AuthError, InputError, ConnectionError
from errors import InvalidRequestError, KeyNotFoundError, UnknownKindError
from extract import Extract
from opinion import Opinion

class List(RequestHandler):
	def check_valid(self):
		if False:
			raise InvalidRequestError('Reason')

	def post(self):
		self.response.content_type='application/json'
		data = {}
		try:
			Auth.check_auth(self.request.headers)
			self.check_valid()
			ts = float(self.request.get('timestamp'))
			logging.debug("Received timestamp : {}".format(ts))

			kinds = self.request.get('kinds')
			if kinds:
				if kinds == 'default':
					kinds = Kind.DEFAULT
				elif kinds == 'all':
					kinds = Kind.SUPPORTED
				else:
					for k in kinds:
						if k not in Kind.SUPPORTED:
							kinds.remove(k)
			else:
				kinds = Kind.DEFAULT

			articles = Opinion.getArticlesAfter(ts)
			entries = []
			uts = ts
			logging.debug(kinds)
			for a in articles:
				if a.kind in kinds:
					uts = (a.date - datetime(1970, 1, 1)).total_seconds()
					e = {}
					e['author'] = a.author
					e['timestamp'] = uts
					e['key'] = a.key
					e['kind'] = a.kind
					e['print_date'] = a.print_date
					e['title'] = a.title
					entries.append(e)
			data['r_timestamp'] = ts
			data['entries'] = entries
			data['num'] = len(entries)
			data['u_timestamp'] = uts

		except AuthError:
			logging.exception('AuthError')
			self.response.set_status(403)
		except InvalidRequestError:
			logging.exception('InvalidRequestError')
			self.response.set_status(400)

		self.response.write(json.dumps(data))

class News(RequestHandler):
	def check_valid(self):
		if False:
			raise InvalidRequestError('Reason')

	def post(self):
		self.response.content_type='application/json'
		data = {}
		try:
			Auth.check_auth(self.request.headers)
			self.check_valid()

			ky = self.request.get('key')
			logging.debug('Recieved key : {}'.format(ky))
			kind, link = Opinion.getKindLink(ky)
			logging.debug('kind for given key : {}'.format(kind))
			logging.debug('Link for given key : {}'.format(link))
			snp = Extract.getHtmlSnippet(kind, link)
			data['snippet'] = snp
			data['key'] = ky
			data['kind'] = kind

		except AuthError:
			logging.exception('AuthError')
			self.response.set_status(403)
			data['error'] = 'You are not authorised to make API calls.'
		except ConnectionError:
			logging.exception('ConnectionError')
			self.response.set_status(504)
		except InputError:
			logging.exception('InputError')
			self.response.set_status(500)
		except InvalidRequestError as e:
			logging.exception('InvalidRequestError')
			self.response.set_status(400)
			data['error'] = e.reason
		except KeyNotFoundError as e:
			self.response.set_status(400)
			data['error'] = 'Key {} not in database.'.format(e.key)
		except UnknownKindError as e:
			self.response.set_status(400)
			data['error'] = 'Key {} corresponds to unsuported kind of article'.format(e.kind)

		self.response.write(json.dumps(data))

app = WSGIApplication([ ('/api/list', List), ('/api/news', News)], debug=True)
