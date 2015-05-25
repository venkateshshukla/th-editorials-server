import cgi
import logging
from webapp2 import RequestHandler, WSGIApplication
from news_db import News

class NewsList(RequestHandler):
	def get(self):
		qry = News.query().order(-News.date)
		self.response.write('<html><body>')
		self.response.write('<h3>List of editorials</h3>')
		i = 0
		for q in qry:
			i += 1
			date = cgi.escape("{:%d-%m-%Y %H:%M:%S}".format(q.date))
			title = cgi.escape(q.title)
			author = cgi.escape(q.author)
			ky = q.get_key()
			href='/news?key={}'.format(ky)
			self.response.out.write('<div><p>')
			self.response.out.write('{}.\t[{}] '.format(i, date))
			self.response.out.write('<a href={}>{}</a>'.format(href, title))
			self.response.out.write('<a href={}>[orig]</a>'.format(q.link))
			if author:
				self.response.out.write(' - {}'.format(author))
			self.response.out.write('</p></div>')
		self.response.write('</body></html>')
	def post(self):
		pass

app = WSGIApplication([ ('/list', NewsList), ], debug=True)
