import hashlib
import logging
from time import mktime
from datetime import datetime
from google.appengine.ext import ndb

class News(ndb.Model):
	"""Class to store news items in GAE NDB"""
	title = ndb.StringProperty(required=True)
	date = ndb.DateTimeProperty(required=True)
	create_date = ndb.DateTimeProperty(auto_now=True)
	link = ndb.StringProperty(required=True)
	author = ndb.StringProperty()
	text = ndb.TextProperty()

	def add_db_unique(self, entry):
		ndate = entry['datetime']
		title = entry['title']
		ptime = entry['print_time']
		link = entry['link']
		author = entry['author']
		text = entry['text']

		ky = hashlib.md5(title + ptime).hexdigest()
		new_key = ndb.Key(News, ky)
		entry = new_key.get()
		if entry is None:
			logging.debug("New news entry found. Adding it to db")
			dt = datetime.fromtimestamp(mktime(ndate))
			news = News(title=title, date=dt, link=link,
					author=author, text=text)
			news.key = new_key
			news.put()
			return True
		else:
			logging.debug("News entry already present. Skipping.")
			return False
