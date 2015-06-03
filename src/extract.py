import logging

from webapp2 import RequestHandler, WSGIApplication

from errors import AuthError InvalidRequestError

class Extract(RequestHandler):
	def post(self):
		try:
			Auth.check_auth(self.request.headers)
			self.check_valid()
		except AuthError:
			logging.exception('AuthError')
			self.response.set_status(403)
		except InvalidRequestError:
			logging.exception('InvalidRequestError')
			self.response.set_status(400)

app = WSGIApplication([ ('/extract', Extract), ], debug=True)
