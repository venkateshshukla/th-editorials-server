from time import mktime
from datetime import datetime
from webapp2 import RequestHandler, WSGIApplication
from google.appengine.ext import ndb
from src.news_feed import get_news_feed
import hashlib

class Feeds(RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		news_list = get_news_feed()
		num_stored = 0
		for n in news_list:
			dt = datetime.fromtimestamp(mktime(n['datetime']))
			title = n['title']
			ky = hashlib.md5(title + n['print_time']).hexdigest()
			new_key = ndb.Key(News, ky)
			entry = new_key.get()
			if entry is None:
				news = News(title=n['title'], date=dt, link=n['link'],
						author=n['author'])
				news.key = ndb.Key(News, ky)
				news.put()
				num_stored += 1
		self.response.write("Number of editorials stored = " +
				str(num_stored))

class News(ndb.Model):
	"""Class to store news items in GAE NDB"""
	title = ndb.StringProperty(required=True)
	date = ndb.DateTimeProperty(required=True)
	create_date = ndb.DateTimeProperty(auto_now=True)
	link = ndb.StringProperty(required=True)
	author = ndb.StringProperty()
	text = ndb.TextProperty()

app = WSGIApplication([ ('/feeds', Feeds), ], debug=True)
