import logging
import time

from datetime import datetime, timedelta
from webapp2 import RequestHandler, WSGIApplication

from constants import Time
from opinion import Opinion

class Clean(RequestHandler):
	def get(self):
		ldate = Opinion.getLastArticleDate()
		dateback = ldate - timedelta(days=Time.EXPIRY)
		midnight = dateback.replace(hour=23, minute=59, second=59)
		logging.debug('Deleting Opinions before {}'.format(midnight))
		timestamp = (midnight - datetime(1970,1, 1)).total_seconds()

		articles = Opinion.deleteOpinionsBefore(timestamp)
		# This pause is necessary to finish the delete operation above.
		time.sleep(Time.SLEEP)

		fdate = Opinion.getFirstArticleDate()
		diff = ldate - fdate
		ref =  timedelta(days=Time.EXPIRY)
		if diff > ref:
			logging.debug('Cleaning failed.')
			self.response.set_status(500)
		else:
			logging.debug('Cleaning successfull.')

app = WSGIApplication([ ('/clean', Clean)], debug=True)
