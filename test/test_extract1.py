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

		self.assertEqual(out, exp, msg="Unsupported tags are also added in output.")


if __name__ == '__main__':
	unittest.main()
