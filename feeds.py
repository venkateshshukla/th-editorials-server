from webapp2 import RequestHandler, WSGIApplication
from src.news_feed import get_news_feed

class Feeds(RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('Editorials!')
		news = get_news_feed()
		for n in news:
			self.response.write("\n\n{}\n{}\n{}\n{}".format(n['title']
				, n['author'], n['print_time'], n['link']))

app = WSGIApplication([ ('/feeds', Feeds), ], debug=True)
