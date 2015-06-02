import logging
import feedparser
from webapp2 import RequestHandler, WSGIApplication

from article import Article
from opinion import Opinion
from constants import AppUrl
from errors import InputError, ParseError, ConnectionError, FeedError, OpinionError

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
	def check_auth(self):
		# Check if the request comes from valid source
		pass
	def check_valid(self):
		# Check if the request is valid
		pass

	def get(self):
		self.check_auth()
		self.check_valid()
		feed = get_feed(AppUrl.OPINION)
		articles = process_feed(feed)
		ins = 0
		for a in articles:
			op = Opinion.fromArticle(a)
			op.add()

app = WSGIApplication([ ('/update', Update), ], debug=True)
