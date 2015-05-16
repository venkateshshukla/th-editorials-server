import requests
import logging
from bs4 import BeautifulSoup
from constants import AppUrl

def get_news_text(url):
	"""Given a url fetch the news html and extract news text."""
	if url is None:
		logging.error("None sent as url.")
		return None

	if not url.startswith(AppUrl.BASE):
		logging.error("Given URL is not recognized.")
		return None

	r = requests.get(url)
	if not r.ok:
		logging.error("Error fetching URL" + str(r.status_code) +
				r.reason)
		return None

	html = r.content
	soup = BeautifulSoup(html)
	news_all = soup.find_all("p")

	if news_all is None:
		logging.error("Element p not found in the HTML")
		return None

	# These comes specifically from studying the HTML layout of website.
	text = u""
	for n in news_all:
		if n is None:
			logging.debug("Found a None p element")
			continue
		elif not n.has_attr("class"):
			logging.debug("Found a p element with no class attribute")
		elif n["class"] == [u"body"]:
			text += n.text
		else:
			logging.debug("Element p is not of body class")
	if text == u"":
		logging.error("Found no element p of class body")
		return None
	return text
