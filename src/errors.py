class Error(Exception):
	"""Base class for exceptions in this module."""
	pass

class ConnectionError(Error):
	"""Exception raised for errors during connection to news server.

	Attributes:
		url -- The url being fetched during error
		status -- The response status returned
	"""
	def __init__(self, url, status):
		self.url = url
		self.status = status

	def __str__(self):
		return "Error {} for {}".format(self.status, self.url)

class ParseError(Error):
	"""Raised when there is error during parsing XML or HTML strings.

	Attributes:
		msg -- The reason for this error
	"""
	def __init__(self, msg):
		self.msg = msg

	def __str__(self):
		return repr(self.msg)

class InputError(Error):
	"""Raised when the given value is malformed or of different type

	Attributes:
		exp -- expected value
		giv -- given value
		msg -- why is the value wrong
	"""
	def __init__(self, exp, giv, msg):
		self.exp = exp
		self.giv = giv
		self.msg = msg
	def __str__(self):
		return "Expected {} Given {} : {}".format(self.exp, self.giv,
				self.msg)

class FeedError(Error):
	"""Raised if any error in dealing with RSS feed"""
	def __init__(self, msg):
		self.msg = msg
	def __str__(self):
		return repr("Feed error : {}.".format(self.msg))

class LinkError(Error):
	"""Raised on encountering improper url"""
	def __init__(self, url):
		self.url = url
	def __str__(self):
		return repr("The URL seems incorrect : {}".format(self.url))

class ArticleError(Error):
	"""Raised on any error in Article class."""
	def __init__(self, msg):
		self.msg = msg
	def __str__(self):
		return repr("Feed error : {}.".format(self.msg))

class OpinionError(Error):
	"""Raised on any error in Opinion class."""
	def __init__(self, msg):
		self.msg = msg
	def __str__(self):
		return repr("Feed error : {}.".format(self.msg))
