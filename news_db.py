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
		title = entry['title']
		link = entry['link']
		author = entry['author']
		text = entry['text']
		ptime = entry['print_time']
		ndate = entry['datetime']
		dt = datetime.fromtimestamp(mktime(ndate))

		ky = hashlib.md5(title).hexdigest()
		new_key = ndb.Key(News, ky)
		entry = new_key.get()
		if entry is None:
			logging.debug("News entry not present. Adding it to db")
			news = News(title=title, date=dt, link=link,
					author=author, text=text)
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
