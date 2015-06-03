import logging
from webapp2 import RequestHandler, WSGIApplication

class Extract(RequestHandler):
	def post(self):
		try:
			Auth.check_auth(self.request.headers)
		except AuthError:
			logging.exception()
			self.response.set_status(403)

app = WSGIApplication([ ('/extract', Extract), ], debug=True)
