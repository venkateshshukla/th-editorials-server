import logging
import requests

from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
from unidecode import unidecode

from constants import AppUrl, Kind, Tags
from errors import ConnectionError, InputError, UnknownKindError

def get_html(url):
	""" Given url, get the html content."""
	if not url:
		raise InputError('url'. url, 'Cannot be empty or None')
	r = requests.get(url)
	if not r.ok:
		raise ConnectionError(url, r.status_code)
	return r.content

def clean_copy(inp, out, soup):
        """
        Recursively copy all the accepted tags and strings from inp to output,
	without getting any of the attributes.

        Args:
                inp : input tag - could be soup object as well
                out : output tag - could be soup object as well
                soup : the actual output soup
        """
        if inp is None or out is None:
                return
        for child in inp.children:
                new = None
                if type(child) is NavigableString:
			s = unidecode(unicode(child.string))
                        new = soup.new_string(s)
                elif type(child) is Tag:
                        if child.name in Tags.accepted:
                                if child.name == 'a':
					s = unidecode(unicode(child.string))
                                        new = soup.new_string(s)
                                else:
                                        new = soup.new_tag(child.name)
                                        clean_copy(child, new, soup)
                        else:
                                logging.debug('Unrecognised tag : {}'.format(child.name))
                else:
                        logging.debug('Unrecognised child : {}'.format(repr(type(child))))

                if new:
                        out.append(new)
        return

def get_article(html):
	"""
	Given the html containing News article, get the news snippet.
	"""
	soup = BeautifulSoup(html)
	out = BeautifulSoup('')
	at = soup.find('div', {'class' : 'article-text'})
	clean_copy(at, out, out)
	return unicode(out).strip()

def get_snippet(kind, html):
	""" Given the kind and the html, get the snippet containing the news"""
	if not html:
		raise InputError('html page', html, 'Cannot be empty or None')
	snp = get_article(html)
	return snp

class Extract:

	@staticmethod
	def getHtmlSnippet(kind, link):
		if not kind:
			raise InputError('kind', kind, 'Cannot be empty or None')
		if not link:
			raise InputError('url', url, 'Cannot be empty or None')
		if kind not in Kind.SUPPORTED:
			raise UnknownKindError(kind)
		logging.debug('kind : {}'.format(kind))
		logging.debug('link : {}'.format(link))
		url = AppUrl.OP_BASE + kind + link
		html = get_html(url)
		snippet = get_snippet(kind, html)
		return snippet
