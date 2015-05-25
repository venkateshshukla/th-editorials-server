import cgi
import logging
from webapp2 import RequestHandler, WSGIApplication
from news_db import News

class NewsText(RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		ky = self.request.get('key')
		news = News()
		entry = news.get_entry_key(ky)
		if entry is None:
			self.response.write('No entry corresponding to the key.')
			self.redirect('/list')
		else:
			self.response.out.write(entry.title)
			self.response.out.write('\n\n{}\t\t\t- {}\n\n'.format(
				entry.date, entry.author))
			self.response.out.write(entry.text)

app = WSGIApplication([ ('/news', NewsText), ], debug=True)
