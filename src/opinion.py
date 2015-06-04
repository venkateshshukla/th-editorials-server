import logging
import hashlib
import json

from datetime import datetime
from unidecode import unidecode
from google.appengine.ext import ndb


from article import Article
from errors import InputError

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
		ky = Opinion.gen_key(title)
		ndb_key = ndb.Key(OpinionList, ky)
		entry = ndb_key.get()
		return entry

	@staticmethod
	def getJsonListStarting(timestamp):
		date = datetime.fromtimestamp(timestamp)
		q = OpinionList.get_by_date(date)
		uts = timestamp
		entries = []
		for o in q:
			uts = (o.date - datetime(1970, 1, 1)).total_seconds()
			e = {}
			e['author'] = o.author
			e['timestamp'] = uts
			e['key'] = o.key.string_id()
			e['kind'] = o.kind
			e['print_date'] = o.print_date
			e['title'] = o.title
			entries.append(e)
		data = {}
		data['r_timestamp'] = timestamp
		data['entries'] = entries
		data['num'] = len(entries)
		data['u_timestamp'] = uts
		return json.dumps(data)

	def add(self):
		entry = Opinion.fetch(self.title)
		if entry is None:
			entry = OpinionList()
			entry.key = ndb.Key(OpinionList,
					self.gen_key(self.title))
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
