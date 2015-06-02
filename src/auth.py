import logging

from errors import AuthError, InputError

class Auth:
	@staticmethod
	def check_auth(headers):
		if not headers:
			raise InputError('headers', headers, 'Cannot be empty or None')
		hd = dict(headers)
		logging.debug("Received request.")
		for h in hd:
			logging.debug("{} : {}".format(repr(h), repr(hd[h])))

