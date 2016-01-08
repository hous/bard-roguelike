#!/usr/bin/python
from __future__ import absolute_import

import sys, os, unittest

sys.path.append(os.path.abspath("./lib"))
sys.path.append(os.path.abspath("./src"))

from sprite import Sprite

class SpriteTestCase(unittest.TestCase):
    """Tests for `sprite.py`."""

    def test_placeholder(self):
        """ Is true true? """
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()