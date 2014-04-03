#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Find missing images.
"""
import os
import gpo_member_photos

if __name__ == "__main__":
    # clone or update legislator YAML
    gpo_member_photos.download_legislator_data()

    legislators = gpo_member_photos.load_yaml(
        "congress-legislators/legislators-current.yaml")
    for l in legislators:
        bioguide = l['id']['bioguide']
        filename = os.path.join("congress", "original", bioguide + ".jpg")
        if not os.path.exists(filename):
            print "---"
            print "Not found:", filename
            print l['name']

# End of file
