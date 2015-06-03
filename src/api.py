import logging

from webapp2 import RequestHandler, WSGIApplication

from auth import Auth
from errors import AuthError, InvalidRequestError

class List(RequestHandler):
	def check_valid(self):
		pass

	def post(self):
		try:
			Auth.check_auth(self.request.headers)
			self.check_valid()
		except AuthError:
			logging.exception()
			self.response.set_status(403)
		except InvalidRequestError:
			logging.exception()
			self.response.set_status(400)

class News(RequestHandler):
	def check_valid(self):
		pass

	def post(self):
		try:
			Auth.check_auth(self.request.headers)
			self.check_valid()
		except AuthError:
			logging.exception()
			self.response.set_status(403)
		except InvalidRequestError:
			logging.exception()
			self.response.set_status(400)

app = WSGIApplication([ ('/api/list', List), ('/api/news', News)], debug=True)
