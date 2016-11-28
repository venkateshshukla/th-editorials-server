import os
import sys
import unittest

from bs4 import BeautifulSoup

sys.path.insert(0, os.path.abspath(".."))

from src.extract import Extract, clean_copy
from src.errors import InputError

class CleanCopyTest(unittest.TestCase):

	def test_none_inp(self):
		inp = None
		out = BeautifulSoup('')
		exp = BeautifulSoup('')

		clean_copy(inp, out, out)

		self.assertEqual(out, exp, msg="Output changes on None input.")

	def test_none_out(self):
		inp = BeautifulSoup('')
		out = None
		soup = BeautifulSoup('<html><body></body></html>')

		clean_copy(inp, out, soup)

		self.assertIsNone(out, msg="Value is assigned to None output.")

	def test_none_soup(self):
		inp = BeautifulSoup('<html><body></body></html>')
		out = BeautifulSoup('')
		soup = None

		self.assertRaises(InputError, clean_copy, inp, out, soup)

	def test_empty_inp(self):
		inp = BeautifulSoup('')
		out = BeautifulSoup('')
		exp = BeautifulSoup('')

		clean_copy(inp, out, out)

		self.assertEqual(out, exp, msg="On empty input, the output is changed.")

	def test_basic_html_without_abip(self):
		inp = BeautifulSoup('<html><head></head><body></body></html>')
		out = BeautifulSoup('')
		exp = BeautifulSoup('')

		clean_copy(inp, out, out)

		self.assertEqual(out, exp, msg="Unsupported tags are also added in output.")

	def test_html_without_abip_2(self):
		inp = BeautifulSoup(
		"""
		<html>
		  <head>
		  </head>
		  <body>
		    <div>
		      <h1>Sample Heading</h1>
		      <h2>Sample Heading</h2>
		      <img src="sample.jpg" alt="example.com" width="100" height="100">
		    </div>
		  </body>
		</html>
		"""
		)
		out = BeautifulSoup("")
		exp = BeautifulSoup("")

		clean_copy(inp, out, out)

		self.assertEqual(unicode(out), unicode(exp))

	def test_html_with_abip(self):
		inp = BeautifulSoup(
			"""
			<html>
			  <head>
			    <title>Sample Title</title>
			  </head>
			  <body>
			    <div class="class_a">
			      <p>This is paragraph 1 of class_a.</p>
			      <a href="http://example.com">This is a link of class_a</a>
			    </div>
			    <div class="class_b">
			      <p>This is paragraph 1 of class_b.</p>
			      <a href="http://example1.com">This is a link of class_b</a>
			      <p>This is <b>paragraph 2</b> of <b>class_a</b>.</p>
			      <a href="http://example2.com">This is a link of <b>class_b</b></a>
			    </div>
			    <div class="class_c">
			      <p>This is paragraph 1 of class_c.</p>
			      <a href="http://example1.com">This is a link of class_c</a>
			      <img alt='sample1' src='sample1.png'>
			      <p>This is <b>paragraph 2</b> of <b>class_c</b>.</p>
			      <a href="http://example2.com">This is a link of <b>class_c<b></a>
			      <img alt='sample2' src='sample2.png'>
			      <p>This is <i>paragraph 3</i> of <i>class_c</i>.</p>
			      <a href="http://example3.com">This is a link of <i>class_c</i></a>
			      <img alt='sample3' src='sample3.png'>
			    </div>
			  </body>
			</html>
			""")
		out = BeautifulSoup("")
		exp = BeautifulSoup(
			"""
			<p>This is paragraph 1 of class_a.</p>
			<p>This is paragraph 1 of class_b.</p>
			<a>This is a link of class_b</a>
			<p>This is <b>paragraph 2</b> of <b>class_a</b>.</p>
			<a>This is a link of <b>class_b</b></a>
			<p>This is paragraph 1 of class_c.</p>
			<a>This is a link of class_c</a>
			<p>This is <b>paragraph 2</b> of <b>class_c</b>.</p>
			<a>This is a link of <b>class_c<b></a>
			<p>This is <i>paragraph 3</i> of <i>class_c</i>.</p>
			<a>This is a link of <i>class_c</i></a>
			""")

		clean_copy(inp, out, out)

		self.assertEqual(unicode(out), unicode(exp))

                def test_format_2911(self):
                    html = """
                    <html>
                      <head>
                        <title>Sample Title</title>
                      </head>
                      <body>
                        <div class="class_a">
                          <p>This is paragraph 1 of class_a.</p>
                          <a href="http://example.com">This is a link of class_a</a>
                        </div>
                        <div class="class_b">
                          <p>This is paragraph 1 of class_b.</p>
                          <a href="http://example1.com">This is a link of class_b</a>
                          <p>This is <b>paragraph 2</b> of <b>class_a</b>.</p>
                          <a href="http://example2.com">This is a link of <b>class_b</b></a>
                        </div>
                        <div class="class_c">
                          <p>This is paragraph 1 of class_c.<strong>
                            <a href="http://example1.com">This is a link of class_c</a></strong>
                          </p>
                          <p>This is <b>paragraph 2</b> of <b>class_c</b>.
                            <small><a href="http://example2.com">This is a link of <b>class_c<b></a></small>
                          </p>
                          <p>This is <i>paragraph 3</i> of <i>class_c</i>
                            <em><a href="http://example3.com">This is a link of <i>class_c</i></a></em>
                          </p>
                        </div>
                      </body>
                    </html>
                    """
                    exp = BeautifulSoup(
                    """
			<p>This is paragraph 1 of class_a.</p>
			<a>This is a link of class_a</a>
			<p>This is paragraph 1 of class_b.</p>
			<a>This is a link of class_b</a>
			<p>This is <b>paragraph 2</b> of <b>class_a</b>.</p>
			<a>This is a link of <b>class_b</b></a>
			<p>This is paragraph 1 of class_c.<strong><a>This is a link of class_c</a></strong></p>
			<p>This is <b>paragraph 2</b> of <b>class_c</b>.<small><a>This is a link of <b>class_c<b></a></small></p>
			<p>This is <i>paragraph 3</i> of <i>class_c</i>.<em><a>This is a link of <i>class_c</i></a></em></p>
                    """)
                    inp = BeautifulSoup(html)
                    out = BeautifulSoup('')
                    clean_copy(inp, out, out)
                    self.assertEqual(unicode(out), unicode(exp))
                    pass

if __name__ == '__main__':
	unittest.main()
