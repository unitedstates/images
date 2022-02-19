#!/usr/bin/env python
"""
Unit tests for gpo_member_photos.py.
Run from root `images` dir:
`python test/test_gpo_member_photos.py`
"""
import datetime
import os
import sys
import unittest

sys.path.insert(0, "scripts")
import gpo_member_photos  # noqa: E402


class TestSequenceFunctions(unittest.TestCase):
    def test_save_metadata(self):
        """Test file is saved"""
        bioguide_id = "A000000"
        gpo_member_photos.save_metadata(bioguide_id)
        self.assertTrue(os.path.exists("congress/metadata/A000000.yaml"))

    def test_resize_photos(self):
        """Test callable"""
        gpo_member_photos.resize_photos()

    def test_pause(self):
        """Test pause delays"""
        # Arrange
        last_request_time = None
        delay = 1
        delta = datetime.timedelta(seconds=delay)

        # Act
        time0 = datetime.datetime.now()
        last_request_time = gpo_member_photos.pause(last_request_time, delay)
        time1 = datetime.datetime.now()
        last_request_time = gpo_member_photos.pause(last_request_time, delay)
        time2 = datetime.datetime.now()

        # Assert
        self.assertLess(time1 - time0, delta)
        self.assertGreaterEqual(time2 - time1, delta)


if __name__ == "__main__":
    unittest.main()

# End of file
