import logging
import hashlib

from unidecode import unidecode
from google.appengine.ext import ndb


from article import Article
from errors import InputError, EntryExistError, EntryDoesntExistError

class Opinion(Article):
	"""Class to store opinion articles"""

	def __init__(self, author, date, kind, link, title):
		Article.__init__(self, author, date, kind, link, title)


	@classmethod
	def fromArticle(cls, article):
		if not article:
			raise InputError("article", article, "Cannot be None")
		return cls(article.author,
				article.date,
				article.kind,
				article.link,
				article.title)

	@staticmethod
	def exists(title):
		if not title:
			raise InputError("title", title, "Cannot be empty or None.")
		ky = Opinion.gen_key(self.title)
		ndb_key = ndb.Key(OpinionList, ky)
		entry = ndb_key.get()
		if entry is None:
			return False
		else:
			return True

	@staticmethod
	def fetch(title):
		if not title:
			raise InputError("title", title, "Cannot be empty or None.")
		ky = Opinion.gen_key(self.title)
		ndb_key = ndb.Key(OpinionList, ky)
		entry = ndb_key.get()
		return entry

	def insert(self):
		entry = Opinion.fetch(self.title)
		if entry:
			raise EntryExistError()
		else:
			logging.info("Adding {} to db.".format(self.title))
			op = OpinionList(author=self.author,
					date = self.date,
					kind = self.kind,
					link = self.link,
					title = self.title)
			op.key = ndb_ky
			op.put()
	def update(self):
		entry = Opinion.fetch(self.title)
		if not entry:
			raise EntryDoesntExistError()
		else:
			logging.info("Updating {}.".format(self.title))
			entry.author = self.author
			entry.date = self.date
			entry.kind = self.kind
			entry.link = self.link
			entry.put()

	def add(self):
		ky = Opinion.gen_key(self.title)
		ndb_key = ndb.Key(OpinionList, ky)
		entry = ndb_key.get()
		if entry is None:
			entry = OpinionList()
			entry.key = ndb_key
		entry.author = self.author
		entry.date = self.date
		entry.kind = self.kind
		entry.link = self.link
		entry.title = self.title
		entry.put()


class OpinionList(ndb.Model):
	"""Class to store news items in GAE NDB"""
	author = ndb.StringProperty(required=True)
	create_date = ndb.DateTimeProperty(auto_now=True)
	date = ndb.DateTimeProperty(required=True)
	kind = ndb.StringProperty(required=True)
	link = ndb.StringProperty(required=True)
	title = ndb.StringProperty(required=True)
