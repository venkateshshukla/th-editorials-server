import logging
from webapp2 import RequestHandler, WSGIApplication

class Extract(RequestHandler):
	def get(self):
		pass
	def post(self):
		pass

app = WSGIApplication([ ('/extract', Extract), ], debug=True)
