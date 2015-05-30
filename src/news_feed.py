import feedparser
import logging
from constants import AppUrl
from errors import ParseError, ConnectionError, InputError
from unidecode import unidecode


def get_news_type(url):
	""" Given the news url, find out the kind of editorial it is"""
	if url is None:
		raise InputError("URL", url, "None url")
	l = url.split('/')
	if len(l) < 6:
		raise InputError("Proper URL", url, "The URL seems to be wrong")
	typ = l[4]
	logging.debug("Got a news item of type : " + typ)
	return typ

def get_news_feed():
	feed = feedparser.parse(AppUrl.OPINION)
	if feed is None:
		raise InputError("RSS feed", feed, "None RSS feed")

	if feed.bozo:
		exc = feed.bozo_exception
		raise ParseError('Bozo bit set. Ill-formed XML.')

	if 'status' not in feed:
		raise ParseError('No status in extracted feed.')

	logging.debug('Feed extraction status : ' + str(feed['status']))

	if feed['status'] != 200:
		raise ConnectionError(AppUrl.OPINION, feed['status'])

	news = []
	for entry in feed['entries']:
		title = unidecode(entry['title'])
		author = unidecode(entry['author'])
		date = entry['published']
		link = entry['link'].replace(AppUrl.RSS_ARGS, '')
		try:
			typ = get_news_type(link)
		except InputError:
			logging.exception("InputError is raised.")
			continue

		logging.debug('Extracted item titled {} dated {} authored {}'.format(title,
			date, author))
		item = {}
		item['title'] = title
		item['datetime'] = entry['published_parsed']
		item['link'] = link
		item['print_time'] = date
		item['author'] = author
		item['type'] = typ
		news.append(item)
	logging.debug("Extracted {} news items.".format(len(news)))
	return news
