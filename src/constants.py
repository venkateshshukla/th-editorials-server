class AppUrl:
	"""Class for storing all the URLs used in the application"""
	BASE = "http://www.thehindu.com/"
	OP_BASE = BASE + "opinion/"
	OPINION = OP_BASE + "?service=rss"
	RSS_ARGS = "?utm_source=RSS_Feed&utm_medium=RSS&utm_campaign=RSS_Syndication"

class Kind:
	BLOGS		=	'blogs'
	CARTOON		=	'cartoon'
	COLUMNS		=	'columns'
	EDITORIAL	=	'editorial'
	INTERVIEW	=	'interview'
	LEAD		=	'lead'
	LETTERS		=	'letters'
	OP_ED		=	'op-ed'
	OPEN_PAGE	=	'open-page'
	READERS_ED	=	'Readers-Editor'
	SUNDAY_ANCHOR	=	'sunday-anchor'
	SUPPORTED	=	[BLOGS, COLUMNS, EDITORIAL, INTERVIEW, LEAD,
			LETTERS, OP_ED, OPEN_PAGE, SUNDAY_ANCHOR]
        DEFAULT         =	[COLUMNS, EDITORIAL, INTERVIEW, LEAD, OP_ED,
                        OPEN_PAGE, SUNDAY_ANCHOR]

class SampleUrl:
	BLOGS		=	'/blog-free-for-all/article7180752.ece'
	CARTOON		=	'/article7282991.ece'
	COLUMNS		=	'/manipur-waiting-to-happen/article7286731.ece'
	EDITORIAL	=	'/monsoon-deficiency-and-its-impact/article7286670.ece'
	INTERVIEW	=	'/interview-with-ashraf-ghani/article7154935.ece'
	LEAD		=	'/on-narendra-modis-visit-to-china/article7286675.ece'
	LETTERS		=	'/a-year-hence/article7286826.ece'
	OP_ED		=	'/who-rules-cyberspace/article7286747.ece'
	OPEN_PAGE	=	'/dialysis-and-the-good-life/article7271883.ece'
	READERS_ED	=	'/readers-editor-column-when-i-is-not-about-myself/article7268426.ece'
	SUNDAY_ANCHOR	=	'/fall-in-allocations/article7265269.ece'

class Tags:
	ACCEPTED = ['a', 'b', 'i', 'p']

class Time:
	EXPIRY = 7
	SLEEP = 0.5
