import logging
from webapp2 import RequestHandler, WSGIApplication

class List(RequestHandler):
	def get(self):
		pass
	def post(self):
		pass

app = WSGIApplication([ ('/list', List), ], debug=True)
