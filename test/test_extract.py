import os
import sys
import logging

sys.path.insert(0, os.path.abspath(".."))
from src.extract import Extract
from src.constants import Kind

logging.basicConfig(level=logging.DEBUG)

articles = [
	(Kind.COLUMNS		,	'/fight-against-hunger-too-slow-and-uneven/article7279094.ece'),
	(Kind.EDITORIAL		,	'/against-the-grain/article7279096.ece'),
	(Kind.INTERVIEW		,	'/union-defence-minister-manohar-parrikar-exclusive-interview/article7244933.ece'),
	(Kind.LEAD		,	'/reconstructing-nepal-after-the-earthquake/article7282990.ece'),
	(Kind.OP_ED		,	'/comment-on-justice-sathasivam-running-for-nhrc-office/article7282984.ece'),
	(Kind.OPEN_PAGE		,	'/the-undo-syndrome/article7271879.ece'),
	]

for a in articles:
	snp = Extract.getHtmlSnippet(a[0], a[1])
	print a[0]
	print a[1]
	f = open(a[0] + '.html', 'w')
	f.write(snp)
	f.close()
	print ''
