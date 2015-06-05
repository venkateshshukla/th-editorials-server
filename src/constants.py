class AppUrl:
	"""Class for storing all the URLs used in the application"""
	BASE = "http://www.thehindu.com/"
	OP_BASE = BASE + "opinion/"
	OPINION = OP_BASE + "?service=rss"
	EDITORIAL = OP_BASE + "editorial/?service=rss"
	SAMPLE = BASE +	"op-ed/a-super-visit-in-the-season-of-hope/article7214799.ece"
	RSS_ARGS = "?utm_source=RSS_Feed&utm_medium=RSS&utm_campaign=RSS_Syndication"

class Kind:
	#BLOGS		=	'blogs'
	#CARTOON	=	'cartoon'
	COLUMNS		=	'columns'
	EDITORIAL	=	'editorial'
	INTERVIEW	=	'interview'
	LEAD		=	'lead'
	#LETTERS	=	'letters'
	OP_ED		=	'op-ed'
	OPEN_PAGE	=	'open-page'
	#READERS_ED	=	'Readers-Editor'
	#SUNDAY_ANCHOR	=	'sunday-anchor'

class Tags:
	accepted = ['a', 'b', 'i', 'p']
