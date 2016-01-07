#!/usr/bin/python
from __future__ import absolute_import

import sys, os, unittest

sys.path.append(os.path.abspath("./lib"))
sys.path.append(os.path.abspath("./src"))

from shapes import Rect, Circle

class ShapesTestCase(unittest.TestCase):
	"""Tests for `shapes.py`."""

	def test_intersecting_rectangles(self):
		"""Do intersecting rectagles intersect?"""
		rect1 = Rect(0, 0, 4, 4)
		rect2 = Rect(2, 2, 4, 4)
		self.assertTrue(rect1.intersect(rect2) and rect2.intersect(rect1))

	def test_nonintersecting_rectangles(self):
		"""Do intersecting rectagles intersect?"""
		rect1 = Rect(0, 0, 4, 4)
		rect2 = Rect(5, 5, 4, 4)
		self.assertFalse(rect1.intersect(rect2) and rect2.intersect(rect1))

	def test_intersecting_rectangles_by_area(self):
		rect1 = Rect(0, 0, 4, 4)
		rect2 = Rect(2, 2, 4, 4)
		self.assertTrue(rect1.intersect_by_area(rect2) and rect2.intersect_by_area(rect1))

	def test_nonintersecting_rectangles_by_area(self):
		rect1 = Rect(0, 0, 4, 4)
		rect2 = Rect(5, 5, 4, 4)
		self.assertFalse(rect1.intersect_by_area(rect2) and rect2.intersect_by_area(rect1))

	def test_intersecting_circles(self):
		circle1 = Circle(4, 4, 2)
		circle2 = Circle(5, 5, 2)
		print circle1.area()
		self.assertTrue(circle1.intersect_by_area(circle2) and circle2.intersect_by_area(circle1))

if __name__ == '__main__':
	unittest.main()