import os
import sys
import unittest

from bs4 import BeautifulSoup

sys.path.insert(0, os.path.abspath(".."))

from src.extract import Extract, clean_copy
from src.errors import InputError

class CleanCopyTest(unittest.TestCase):

	def test_empty_inp(self):
		inp = None
		out = BeautifulSoup('')
		soup = BeautifulSoup('<html><body></body></html>')

		exp = out

		clean_copy(inp, out, soup)

		self.assertEqual(out, exp, msg="Output changes on None input.")

	def test_empty_out(self):
		inp = BeautifulSoup('')
		out = None
		soup = BeautifulSoup('<html><body></body></html>')

		clean_copy(inp, out, soup)

		self.assertIsNone(out, msg="Value is assigned to None output.")

	def test_empty_soup(self):
		inp = BeautifulSoup('<html><body></body></html>')
		out = BeautifulSoup('')
		soup = None

		self.assertRaises(InputError, clean_copy, inp, out, soup)

if __name__ == '__main__':
	unittest.main()
