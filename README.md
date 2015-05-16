Get new editorials published in The Hindu
=========================================

Get any new editorials published in The Hindu, the leading english daily in
India.

Dependencies
============
1. Requests		- http://docs.python-requests.org/en/latest/
2. FeedParser		- https://pythonhosted.org/feedparser/
3. BeautifulSoup	- http://www.crummy.com/software/BeautifulSoup/

Deploying to Google App Engine
==============================

Adding feedparser to GAE

Google App Engine supports only certain libraries. For other libraries,
including feedparser, additional steps need to be taken in order to make
it work.

For this, follow these steps

1. Install virtualenv `sudo pip install virtualenv`
2. Create virualenv outside source `virtualenv ../appenv`
3. Activate virtualenv `source ../appenv/bin/activate`
4. Make a lib folder in application source `mkdir lib`
5. Install the dependencies in lib folder using pip `pip install -t lib -r requirements.txt`

And you are done.

Deploy the application to local machine using `dev_appserver.py .`
