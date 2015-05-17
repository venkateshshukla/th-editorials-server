import logging
from news_db import News
from src.news_feed import get_news_feed
from src.news_text import get_news_text
from webapp2 import RequestHandler, WSGIApplication

class Feeds(RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		try:
			news_list = get_news_feed()
		except ConnectionError:
			logging.error("Error connecting to the RSS feed.")
			self.response.write("Error connecting to RSS feed.");
			return
		num_stored = 0
		for n in news_list:
			try:
				n['text'] = get_news_text(n['link'])
			except ConnectionError:
				logging.error("Error fetching news link")
				continue
			news = News()
			if news.add_db_unique(n):
				num_stored += 1
		self.response.write("Number of editorials stored = " +
				str(num_stored))


app = WSGIApplication([ ('/feeds', Feeds), ], debug=True)
