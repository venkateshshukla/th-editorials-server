import feedparser
import logging
from constants import AppUrl

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
		logging.debug('Extracted item dated ' + str(entry['published']))
		item = {}
		item['title'] = entry['title']
		item['datetime'] = entry['published_parsed']
		item['link'] = entry['link']
		item['print_time'] = entry['published']
		item['author'] = entry['author']
		news.append(item)
	return news
