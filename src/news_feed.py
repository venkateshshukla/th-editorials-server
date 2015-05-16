import feedparser
import logging

def get_news_feed():
	editorial_url = "http://www.thehindu.com/opinion/editorial/?service=rss"
	feed = feedparser.parse(editorial_url)
	if feed is None:
		logging.error('RSS Feed is None')
		return None

	if 'status' in feed:
		logging.debug('Feed extraction status : ' + str(feed['status']))

	if feed['status'] != 200:
		logging.error('Failed to extract RSS Feed : error ' +
				str(feed['status']))
		return None

	news = []
	for entry in feed['entries']:
		logging.debug('Extracted item dated ' + str(entry['published']))
		item = (entry['title'], entry['published'], entry['link'])
		news.append(item)

	return news

