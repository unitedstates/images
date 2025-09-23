#!/usr/bin/env python
"""
Scrape https://memberguide.gpo.gov and
save members' photos named after their Bioguide IDs.
"""
import argparse
import datetime
import json
import os
import re
import time
from urllib.error import HTTPError
from urllib.request import urlretrieve

# pip install -r requirements.txt
import mechanicalsoup

CURRENT_CONGRESS = 118

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
)

regex1 = re.compile(
    r'<a href="/member/[^/]+/(\w+)[^<]+</a></span>'
    '[^<]*<div[^<]+<div class="member-image"><img src="/img/member/([^"]+)"'
)

regex2 = re.compile('<a class="next" href="([^"]+)">')


def pause(last, delay):
    if last is None:
        return datetime.datetime.now()

    now = datetime.datetime.now()
    delta = (now - last).total_seconds()

    if delta < delay:
        sleep = delay - delta
        print(f"Sleep for {sleep} seconds")
        time.sleep(sleep)
    return datetime.datetime.now()


def get_members_pictorial(br, congress_number):
    """
    Get members for the given congress_number
    API documentation: https://pictorialapi.gpo.gov/index.html
    """
    response = br.get(
        f"https://pictorialapi.gpo.gov/api/GuideMember/GetMembers/{congress_number}"
    ).json()
    return [
        member
        for member in response["memberCollection"]
        if member["memberType"] in ("Senator", "Representative")
        and member["name"] != "Vacant, Vacant"
    ]


def get_legislators_current(br, include_historical=False):
    """
    Download legislators from sister project unitedstates/congress-legislators
    Optionally also include historical legislators (which significantly
    increases the download size)
    """
    legislators = br.get(
        "https://unitedstates.github.io/congress-legislators/legislators-current.json"
    ).json()
    if include_historical:
        historical = br.get(
            "https://unitedstates.github.io/congress-legislators/"
            "legislators-historical.json"
        ).json()
        legislators += historical
    return legislators


def save_metadata(bioguide_id, photo_source):
    outdir = "congress/metadata"
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    outfile = os.path.join(outdir, bioguide_id + ".yaml")
    with open(outfile, "w") as f:
        if photo_source == "gpo":
            f.write("source: GPO Member Guide\n")
            f.write("source_url: https://pictorial.gpo.gov\n")
        elif photo_source == "congress":
            f.write("source: Congress.gov API\n")
            f.write("source_url: https://api.congress.gov/\n")
        else:
            f.write("source: Unknown\n")


def download_file(url, outfile):
    """Download file at url to outfile"""
    fn, info = urlretrieve(url, outfile)

    # Sanity check we got an image. urlretreive will still save
    # content on a 404. If we didn't get an image, kill the file
    # (since we already saved it, oops) and raise an exception.
    if info["Content-Type"] != "image/jpeg":
        os.unlink(fn)
        raise HTTPError()


def download_photos(br, photo_list, outdir, delay):
    last_request_time = None

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    ok = 0

    for bioguide_id, photo_url, photo_source in photo_list:
        print(bioguide_id, photo_url)

        filename = os.path.join(outdir, bioguide_id + ".jpg")
        if os.path.isfile(filename):
            print(" Image already exists:", filename)
        elif not args.test:
            last_request_time = pause(last_request_time, delay)
            try:
                download_file(photo_url, filename)
            except HTTPError as e:
                print("Image not available:", e)
            else:
                save_metadata(bioguide_id, photo_source)
                ok += 1

    print("Downloaded", ok, "member photos.")
    return ok

def get_congress_gov_photo_url(bioguide_id, api_key):
    """
    Get the photo URL for a member using their bioguide id via the Congress.gov API.
    API documentation: https://api.congress.gov/
    """
    response = br.get(
        f"https://api.congress.gov/v3/member/{bioguide_id}",
        params={"api_key": api_key}
    ).json()
    # Check member, depiction, imageUrl tree of keys
    if "member" in response and "depiction" in response["member"] and "imageUrl" in response["member"]["depiction"]:
        # cut the "_200" width from the URL to get the full-size image
        return response["member"]["depiction"]["imageUrl"].replace("_200", "")
    return None


def resize_photos():
    # Assumes they're congress/original/*.jpg
    os.system(os.path.join("scripts", "resize-photos.sh"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Save members' photos from pictorialapi.gpo.gov, named "
        "after their Bioguide IDs",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-n",
        "--congress",
        default=CURRENT_CONGRESS,
        type=int,
        help="Congress session number, for example: 110, 111, 112, 113",
    )
    parser.add_argument(
        "-o",
        "--outdir",
        default="congress/original",
        help="Directory to save photos in",
    )
    parser.add_argument(
        "-d",
        "--delay",
        type=int,
        default=5,
        metavar="seconds",
        help="Rate-limiting delay between scrape requests",
    )
    parser.add_argument(
        "-k",
        "--key",
        help="API key for authentication (if required for congress.gov API)",
    )
    parser.add_argument(
        "-t",
        "--test",
        action="store_true",
        help="Test mode: don't actually save images",
    )
    args = parser.parse_args()

    br = mechanicalsoup.Browser()
    br.set_user_agent(USER_AGENT)

    legislators_current = get_legislators_current(br, args.congress != CURRENT_CONGRESS)
    members_pictorial = get_members_pictorial(br, args.congress)

    photo_list = []
    errors = []
    for m in legislators_current:
        image_found = False
        if "pictorial" in m["id"]:
            try:
                pictorial_data = next(
                    p
                    for p in members_pictorial
                    if p["memberId"] == m["id"]["pictorial"]
                )

                if "nophotoimage.jpg" in pictorial_data["imageUrl"]:
                    pass
                else:
                    image_found = True
                    photo_list.append((m["id"]["bioguide"], pictorial_data["imageUrl"], "gpo"))
            except StopIteration:
                # No matching result from pictorial API
                pass

        # Try congress.gov ID depiction if pictorial ID not found
        # and we have a congress.gov ID
        if not image_found and args.key:
            image = get_congress_gov_photo_url(m["id"]["bioguide"], args.key)
            if image:
                image_found = True
                photo_list.append((m["id"]["bioguide"], image, "congress"))

        if not image_found:
            print(f"No photo available for {m['id']['bioguide']}")
            errors.append(["No photo available", m["id"]["bioguide"], m["name"]])

    number = download_photos(br, photo_list, args.outdir, args.delay,)

    if number:
        resize_photos()

    if len(errors):
        print(f"{len(errors)} legislators had errors. Details wrote to errors.json")
        with open("errors.json", "w") as f:
            json.dump(errors, f, indent=2)

# End of file
