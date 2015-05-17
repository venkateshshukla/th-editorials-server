import feedparser
import logging
from constants import AppUrl
from unidecode import unidecode

def get_news_feed():
	feed = feedparser.parse(AppUrl.OPINION)
	if feed is None:
		logging.error('RSS Feed is None')
		return None

	if feed.bozo:
		logging.error('Bozo bit set. Ill-formed XML encountered.')
		return None

	if 'status' not in feed:
		logging.error('No status in extracted feed.')
		return None

	logging.debug('Feed extraction status : ' + str(feed['status']))

	if feed['status'] != 200:
		logging.error('Failed to extract RSS Feed : error ' +
				str(feed['status']))
		return None

	news = []
	for entry in feed['entries']:
		title = unidecode(entry['title'])
		date = entry['published']
		link = entry['link'].replace(AppUrl.RSS_ARGS, '')
		logging.debug('Extracted item titled {} dated {}'.format(title,	date))
		item = {}
		item['title'] = title
		item['datetime'] = entry['published_parsed']
		item['link'] = link
		item['print_time'] = date
		item['author'] = entry['author']
		news.append(item)
	logging.debug("Extracted {} news items.".format(len(news)))
	return news
