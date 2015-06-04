import logging
import feedparser
import hashlib
import time

from unidecode import unidecode
from datetime import datetime

from errors import InputError, LinkError
from constants import AppUrl

class Article:
	"""Class to store opinion articles"""
	def __init__(self, author, date, kind, link, pdate, title):
		self.author =  Article.process(author)
		self.date = date
		self.link =  Article.process(link)
		self.kind =  Article.process(kind)
		self.print_date = pdate
		self.title = Article.process(title)
		self.validate()

	def validate(self):
		# Check if the attributes are empty or None
		if self.author is None:
			raise InputError("author", self.author, "Cannot be None")
		if not self.kind:
			raise InputError("kind", self.kind, "Cannot be empty or None")
		if not self.link:
			raise InputError("link", self.link, "Cannot be empty or None")
		if not self.print_date:
			raise InputError("print_date", self.print_date, "Cannot be empty or None")
		if not self.title:
			raise InputError("title", self.title, "Cannot be empty or None")
		if self.date is None:
			raise InputError('datetime object', self.date, "Cannot be None")
		# if self.date is not in range (that is acceptable last date and now)
		# raise InputError("date", self.date, "Range is incorrect.")

	@staticmethod
	def process(stuff):
		# String whitespaces and transliterate unicode
		if isinstance(stuff, unicode):
			return unidecode(stuff).strip()
		elif isinstance(stuff, str):
			return stuff.strip()
		else:
			raise InputError("unicode or str", stuff, "Cannot be anything other than unicode or string.")

	@staticmethod
	def gen_key(title):
		# Given the title, generate a unique key of the article
		if not title:
			raise InputError("title", title, "Cannot be empty or None.")
		ky = hashlib.sha1(title).hexdigest()
		return ky


	@classmethod
	def fromFeedParserDict(cls, entry):
		# Given a feedparser.FeedParserDict, create an article
		if not entry:
			raise InputError("FeedParserDict", entry, "Cannot be None")

		if not isinstance(entry, feedparser.FeedParserDict):
			raise InputError("FeedParserDict", entry, "Cannot be anything else.")

		def get_link(raw_link, kind):
			if not raw_link:
				raise InputError("Link", raw_link, "Cannot be empty or None")

			if not kind:
				raise InputError("Kind", kind, "Cannot be empty or None")
			a = raw_link.replace(AppUrl.RSS_ARGS, '')
			b = a.replace(AppUrl.OP_BASE, '')
			c = b.replace(kind, '')
			logging.debug("Article link : {}".format(c))
			return c

		def get_kind(raw_link):
			if not raw_link:
				raise InputError("Link", raw_link, "Cannot be empty or None")
			a = raw_link.replace(AppUrl.RSS_ARGS, '')
			b = a.split('/')
			if len(b) < 6:
				raise LinkError(raw_link)
			kind = b[4]
			logging.debug("Article kind : {}".format(kind))
			return kind

		def get_date(tm):
			if not isinstance(tm, time.struct_time):
				raise InputError("time.struct_time", tm,
						"Should be time.struct_time")
			return datetime.fromtimestamp(time.mktime(tm))

		title = entry['title']
		author = entry['author']
		raw_link = entry['link']
		print_date = entry['published']
		date = get_date(entry['published_parsed'])

		try:
			kind = get_kind(raw_link)
			link = get_link(raw_link, kind)
		except InputError:
			logging.exception("InputError is raised.")
			return None

		return cls(author, date, kind, link, print_date, title)
