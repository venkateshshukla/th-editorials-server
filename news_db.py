import hashlib
import logging
from time import mktime
from datetime import datetime
from google.appengine.ext import ndb
from src.errors import InputError

class News(ndb.Model):
	"""Class to store news items in GAE NDB"""
	title = ndb.StringProperty(required=True)
	date = ndb.DateTimeProperty(required=True)
	create_date = ndb.DateTimeProperty(auto_now=True)
	link = ndb.StringProperty(required=True)
	author = ndb.StringProperty()
	text = ndb.TextProperty()
	news_type = ndb.StringProperty(required=True)

	def add_db_unique(self, entry):
		""" Given an entry dict, add it to ndb. Make sure its unique."""
		if entry is None:
			raise InputError("Entry", entry, "Entry cannot be None.")
		title = entry['title']
		link = entry['link']
		author = entry['author']
		text = entry['text']
		ptime = entry['print_time']
		ndate = entry['datetime']
		dt = datetime.fromtimestamp(mktime(ndate))
		typ = entry['type']

		ky = hashlib.md5(title).hexdigest()
		new_key = ndb.Key(News, ky)
		entry = new_key.get()
		if entry is None:
			logging.debug("News entry not present. Adding it to db")
			news = News(title=title, date=dt, link=link,
					author=author, text=text, news_type=typ)
			news.key = new_key
			news.put()
			return True
		else:
			logging.debug("News entry already present.")
			if entry.date == dt:
				logging.debug("News entry has same date. Skipping.")
				return False
			else:
				logging.debug("News entry has new date.	Updating.")
				entry.date = dt
				entry.put()
				return True

	def get_entry_key(self, ky):
		"""For the given key, return the corresponding entry from ndb."""
		if ky is None:
			raise InputError("Key", ky, "Key cannot be None.")
		n_key = ndb.Key(News, ky)
		entry = n_key.get()
		if entry is None:
			logging.error("No entry for given key.")
			return None
		else:
			return entry

	def get_key(self):
		"""Return the key of this entry."""
		if self.title is None:
			logging.debug("Unable to generate key due to None entry.")
			return None
		else:
			return hashlib.md5(self.title).hexdigest()
