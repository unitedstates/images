#!/usr/bin/env python
"""
Find missing images.
"""
import os

# pip install -r requirements.txt
import yaml


# Make sure we have the congress-legislators repository available.
def download_legislator_data():
    # clone it if it's not out
    if not os.path.exists("congress-legislators"):
        print("Cloning the congress-legislators repo...")
        os.system(
            "git clone -q --depth 1 "
            "https://github.com/unitedstates/congress-legislators "
            "congress-legislators"
        )

    # Update the repo so we have the latest.
    print("Updating the congress-legislators repo...")
    # these two == git pull, but git pull ignores -q on the merge part
    # so is less quiet
    os.system(
        "cd congress-legislators; git fetch -pq; "
        "git merge --ff-only -q origin/master"
    )


def load_yaml(filename):
    f = open(filename)
    data = yaml.safe_load(f)
    f.close()
    return data


def file_exists(filename):
    if not os.path.exists(filename):
        print("---")
        print("Not found:", filename)
        print(legislator["name"])
        return False
    return True


if __name__ == "__main__":
    # clone or update legislator YAML
    download_legislator_data()

    legislators = load_yaml("congress-legislators/legislators-current.yaml")
    for legislator in legislators:
        bioguide = legislator["id"]["bioguide"]
        filename = os.path.join("congress", "original", bioguide + ".jpg")
        if file_exists(filename):
            # Only check for yaml if jpg exists
            filename = os.path.join("congress", "metadata", bioguide + ".yaml")
            file_exists(filename)

# End of file
