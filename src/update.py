import logging
import feedparser
from webapp2 import RequestHandler, WSGIApplication

from auth import Auth
from article import Article
from opinion import Opinion
from constants import AppUrl
from errors import AuthError, ConnectionError, FeedError, InputError

def get_feed(url):
	""" Given url of an RSS feed, fetch feedparser object."""
	if not url:
		raise InputError("URL", url, "Cannot be empty or None")

	feed = feedparser.parse(url)

	if feed is None:
		raise FeedError("RSS feed", feed, "None RSS feed")

	if feed.bozo:
		exc = feed.bozo_exception
		raise FeedError('Bozo bit set. Reason : {}.'.format(repr(exc)))

	if 'status' not in feed:
		raise FeedError('No status in extracted feed.')

	logging.debug('Feed extraction status : ' + str(feed['status']))

	if feed['status'] != 200:
		raise ConnectionError(url, feed['status'])

	return feed

def process_feed(feed):
	if not feed:
		raise InputError("feedparser object", feed, "Cannot be None.")
	articles = []
	for entry in feed['entries']:
		a = Article.fromFeedParserDict(entry)
		if a:
			articles.append(a)
	logging.debug("Extracted {} news items.".format(len(articles)))
	return articles

class Update(RequestHandler):
	def get(self):
		try:
			Auth.check_auth(self.request.headers)
			feed = get_feed(AppUrl.OPINION)
			articles = process_feed(feed)
			ins = 0
			for a in articles:
				op = Opinion.fromArticle(a)
				op.add()
		except AuthError:
			logging.exception('AuthError')
			self.response.set_status(403)
		except ConnectionError:
			logging.exception('ConnectionError')
			self.response.set_status(504)
		except FeedError:
			logging.exception('Feed Error')
			self.response.set_status(500)
		except InputError:
			logging.exception('InputError')
			self.response.set_status(500)

app = WSGIApplication([ ('/update', Update), ], debug=True)
