#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unit tests for gpo_member_photos.py.
Run from root `images` dir:
`python test/test_gpo_member_photos.py`
"""
from __future__ import print_function, unicode_literals
import os
import sys
try:
    import unittest2 as unittest
except ImportError:
    import unittest

sys.path.insert(0, 'scripts')
import gpo_member_photos


class TestSequenceFunctions(unittest.TestCase):

    def test_save_metadata(self):
        """ Test file is saved """
        bioguide_id = "A000000"
        gpo_member_photos.save_metadata(bioguide_id)
        self.assertTrue(os.path.exists("congress/metadata/A000000.yaml"))

    def test_resize_photos(self):
        """ Test callable """
        gpo_member_photos.resize_photos()

if __name__ == '__main__':
    unittest.main()

# End of file
