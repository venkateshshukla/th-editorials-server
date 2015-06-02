import logging

from errors import AuthError, InputError

class Auth:
	@staticmethod
	def check_auth(headers):
		if not headers:
			raise InputError('headers', headers, 'Cannot be empty or None')
		hd = dict(headers)
		logging.debug("Received request.")
		logging.debug("Host : {}".format(repr(headers['Host'])))
		logging.debug("User-Agent : {}".format(repr(headers['User-Agent'])))
