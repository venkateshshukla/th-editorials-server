import os
import sys
import logging

sys.path.insert(0, os.path.abspath(".."))
from src.extract import Extract
from src.constants import Kind

logging.basicConfig(level=logging.DEBUG)

articles = [
	(Kind.COLUMNS		,	Sample.COLUMNS),
	(Kind.EDITORIAL		,	Sample.EDITORIAL),
	(Kind.INTERVIEW		,	Sample.INTERVIEW),
	(Kind.LEAD		,	Sample.LEAD),
	(Kind.OP_ED		,	Sample.OP_ED),
	(Kind.OPEN_PAGE		,	Sample.OPEN_PAGE),
	]

for a in articles:
	snp = Extract.getHtmlSnippet(a[0], a[1])
	print a[0]
	print a[1]
	f = open(a[0] + '.html', 'w')
	f.write(snp)
	f.close()
	print ''
