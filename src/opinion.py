import logging
import hashlib

from datetime import datetime
from unidecode import unidecode
from google.appengine.ext import ndb


from article import Article
from errors import InputError, KeyNotFoundError
from constants import AppUrl

class Opinion(Article):
	"""Class to store opinion articles"""

	def __init__(self, author, date, kind, link, pdate, title):
		Article.__init__(self, author, date, kind, link, pdate, title)

	@classmethod
	def fromArticle(cls, article):
		if not article:
			raise InputError("article", article, "Cannot be None")
		return cls(article.author,
				article.date,
				article.kind,
				article.link,
				article.print_date,
				article.title)

	@staticmethod
	def getArticlesAfter(timestamp):
		"""
		Given a timestamp, return a list of newer articles.
		"""
		date = datetime.fromtimestamp(timestamp)
		query = OpinionList.get_by_date(date)
		articles = []
		for q in query:
			articles.append(Article(q.author, q.date, q.kind,
				q.link, q.print_date, q.title))
		return articles

	@staticmethod
	def getKindLink(ky):
		e = OpinionList.get_by_key(ky)
		if e:
			return e.kind, e.link
		else:
			raise KeyNotFoundError(ky)

	def fetch(self):
		ndb_key = ndb.Key(OpinionList, self.key)
		entry = ndb_key.get()
		return entry

	def add(self):
		entry = self.fetch()
		if entry is None:
			entry = OpinionList()
			entry.key = ndb.Key(OpinionList, self.key)
		entry.author = self.author
		entry.date = self.date
		entry.kind = self.kind
		entry.link = self.link
		entry.print_date = self.print_date
		entry.title = self.title
		entry.put()

class OpinionList(ndb.Model):
	"""Class to store news items in GAE NDB"""
	author = ndb.StringProperty(required=True)
	create_date = ndb.DateTimeProperty(auto_now=True)
	date = ndb.DateTimeProperty(required=True)
	kind = ndb.StringProperty(required=True)
	link = ndb.StringProperty(required=True)
	print_date = ndb.StringProperty(required=True)
	title = ndb.StringProperty(required=True)

	@classmethod
	def get_by_date(cls, date):
		return cls.query(cls.date > date).order(cls.date)

	@classmethod
	def get_by_key(cls, ky):
		key = ndb.Key(cls, ky)
		return key.get()
