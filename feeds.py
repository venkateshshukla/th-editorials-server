from news_db import News
from src.news_feed import get_news_feed
from src.news_text import get_news_text
from webapp2 import RequestHandler, WSGIApplication

class Feeds(RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		news_list = get_news_feed()
		num_stored = 0
		for n in news_list:
			n['text'] = get_news_text(n['link'])
			news = News()
			if news.add_db_unique(n):
				num_stored += 1
		self.response.write("Number of editorials stored = " +
				str(num_stored))


app = WSGIApplication([ ('/feeds', Feeds), ], debug=True)
