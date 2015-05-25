import requests
import logging
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Comment
from constants import AppUrl
from errors import ConnectionError, ParseError, InputError

def print_tags(tag):
	"""For given tag, print the tags of all the children"""
	for c in tag.children:
		if c.name is None:
			print "None", '\t\t', repr(c)
		else:
			print c.name, '\t\t', repr(c)

def _extract_text(html):
	"""Given the html file, extract the text from it"""
	if html is None:
		raise InputError("HTML is not supposed to be None")

	soup = BeautifulSoup(html)

	if soup is None:
		raise ParseError("Soup not made. Is HTML valid?")

	news_all = soup.find_all('p')
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
		elif u"body" in n["class"]:
			logging.debug("Found news element. Extracting tag.")
			text += _extract_text_tag(n)
		else:
			logging.debug("Element p is not of body class")
	if text == u"":
		raise ParseError("Found no element p of class body")

	logging.debug("News text extracted. Returning.")
	return text

def _extract_text_tag(tag):
	"""Given BeautifulSoup Tag element, extract the news"""
	if tag is None:
		raise InputError("tag cannot be None")
	accepted_name = [None, 'i', 'b']
	text = ""
	for c in tag.children:
		if c.name in accepted_name:
			if isinstance(c.string, NavigableString):
				logging.debug("Found a navigable string.")
				text += c.string
			elif isinstance(c.string, Comment):
				logging.debug("Found comment string : " +
						c.string)
			else:
				logging.debug("Found an element neither a navigable nor a comment string.")
	if text == "":
		logging.warning("No text found in the html tag")
	else:
		logging.debug("Some text found. Returning.")
	return text


def get_news_text(url):
	"""Given a url fetch the news html and extract news text."""
	if url is None:
		raise InputError("URL", "None", "None object.")

	if not url.startswith(AppUrl.BASE):
		raise InputError("Known URL", url, "Unrecongised URL")

	surl = url.replace(AppUrl.BASE, '')
	logging.debug("News url recieved : " + surl)

	try:
		r = requests.get(url)
	except request.exceptions.ConnectionError:
		raise ConnectionError(surl, 0)

	if not r.ok:
		raise ConnectionError(surl , r.status_code)

	logging.debug("HTML of news url fetched. Making a soup.")
	html = r.content
	text = _extract_text(html)
	return text
