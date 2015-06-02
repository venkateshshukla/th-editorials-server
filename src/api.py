import logging

from webapp2 import RequestHandler, WSGIApplication

from auth import Auth
from errors import AuthError

class List(RequestHandler):
	def post(self):
		try:
			Auth.check_valid(self.response.headers)
		except AuthError:
			logging.exception()
			self.response.set_status(403)

class News(RequestHandler):
	def post(self):
		try:
			Auth.check_valid(self.response.headers)
		except AuthError:
			logging.exception()
			self.response.set_status(403)

app = WSGIApplication([ ('/api/list', List), ('/api/news', News)], debug=True)
