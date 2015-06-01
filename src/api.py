import logging
from webapp2 import RequestHandler, WSGIApplication

class List(RequestHandler):
	def get(self):
		pass
	def post(self):
		pass

class News(RequestHandler):
	def get(self):
		pass
	def post(self):
		pass

app = WSGIApplication([ ('/api/list', List), ('/api/news', News)], debug=True)
