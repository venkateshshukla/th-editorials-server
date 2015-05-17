import requests
import logging
from bs4 import BeautifulSoup
from constants import AppUrl
from errors import ConnectionError, ParseError, InputError

def get_news_text(url):
	"""Given a url fetch the news html and extract news text."""
	if url is None:
		raise InputError("URL", "None", "None object.")

	if not url.startswith(AppUrl.BASE):
		raise InputError("Known URL", url, "Unrecongised URL")

	surl = url.replace(AppUrl.BASE, '')
	logging.debug("News url recieved : " + surl)
	r = requests.get(url)
	if not r.ok:
		raise ConnectionError(surl , r.status_code)

	logging.debug("HTML of news url fetched. Making a soup.")
	html = r.content
	soup = BeautifulSoup(html)
	news_all = soup.find_all("p")

	if news_all is None:
		raise ParseError("Error finding element p in HTML")

	if len(news_all) == 0:
		raise ParseError("Element p not found in the HTML")

	logging.debug("Some p elements present in HTML. Getting text.")
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
		raise ParseError("Found no element p of class body")

	logging.debug("News text extracted. Returning.")
	return text
