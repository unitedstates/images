#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Find missing images.
"""
from __future__ import print_function
import os
import gpo_member_photos


def file_exists(filename):
    if not os.path.exists(filename):
        print("---")
        print("Not found:", filename)
        print(l['name'])
        return False
    return True


if __name__ == "__main__":
    # clone or update legislator YAML
    gpo_member_photos.download_legislator_data()

    legislators = gpo_member_photos.load_yaml(
        "congress-legislators/legislators-current.yaml")
    for l in legislators:
        bioguide = l['id']['bioguide']
        filename = os.path.join("congress", "original", bioguide + ".jpg")
        if file_exists(filename):
            # Only check for yaml if jpg exists
            filename = os.path.join("congress", "metadata", bioguide + ".yaml")
            file_exists(filename)

# End of file
