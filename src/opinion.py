import logging
import hashlib
import time

from datetime import datetime
from unidecode import unidecode
from google.appengine.ext import ndb


from article import Article
from errors import InputError, EmptyDatabaseError, EntryNotFoundError
from errors import KeyNotFoundError
from constants import AppUrl

class Opinion(Article):
	"""Class to store opinion articles"""

	def __init__(self, author, date, kind, link, pdate, title):
		Article.__init__(self, author, date, kind, link, pdate, title)

	@staticmethod
	def deleteOpinionsBefore(timestamp):
		"""
		Given a timestamp, return a list of newer articles.
		"""
		date = datetime.fromtimestamp(timestamp)
		query = OpinionList.get_before_date(date)
		keys = []
		for q in query:
			logging.debug('Deleting Opinion dated {} titled {}.'.format(q.date, q.title))
			keys.append(q.key)
		ndb.delete_multi(keys)
		logging.debug('Deleted {} Opinions.'.format(len(keys)))

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
	def getFirstArticleDate():
		"""
		Find the date of the earliest article present in the datastore.
		"""
		article = OpinionList.get_earliest()
		if not article:
			raise EmptyDatabaseError()
		date = article.date
		logging.debug("Date of the earliest article : {}".format(date))
		return date

	@staticmethod
	def getLastArticleDate():
		"""
		Find the date of the latest article present in the datastore.
		"""
		article = OpinionList.get_latest()
		while not article:
			raise EmptyDatabaseError()
		date = article.date
		logging.debug("Date of the latest article : {}".format(date))
		return date

	@staticmethod
	def getArticlesAfter(timestamp):
		"""
		Given a timestamp, return a list of newer articles.
		"""
		date = datetime.fromtimestamp(timestamp)
		query = OpinionList.get_after_date(date)
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

	@staticmethod
	def getInfo(ky):
		e = OpinionList.get_by_key(ky)
		if e:
			return {
				'author' : e.author,
				'date' : e.print_date,
				'kind' : e.kind,
				'link' : e.link,
				'title' : e.title
				}
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
	def get_before_date(cls, date):
		return cls.query(cls.date < date).order(cls.date)

	@classmethod
	def get_after_date(cls, date):
		return cls.query(cls.date > date).order(cls.date)

	@classmethod
	def get_by_key(cls, ky):
		key = ndb.Key(cls, ky)
		return key.get()

	@classmethod
	def get_latest(cls):
		return cls.query().order(-cls.date).get()

	@classmethod
	def get_earliest(cls):
		return cls.query().order(cls.date).get()
