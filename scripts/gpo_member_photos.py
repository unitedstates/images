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
import sys
import time
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlretrieve

# pip install -r requirements.txt
import mechanicalsoup

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


def get_photo_list(br, congress_number, delay):
    last_request_time = None

    page = 1
    while True:
        # Fetch a page of results from Congress.gov.
        print(f"Page {page} of Congress.gov Member listing...")
        response = br.get(
            "https://www.congress.gov/search?"
            + urlencode(
                {
                    "q": json.dumps(
                        {"source": "members", "congress": str(congress_number)}
                    ),
                    "pageSize": 250,
                    "page": page,
                }
            )
        ).text

        if len(response) == 0:
            sys.exit("Page is blank. Try again later, you may have hit a limit.")

        # Scan for links to Member pages and img tags. The link to the
        # Congress.gov page uses the Member's Bioguide ID as the key, and the
        # filename for the photo is the same file name found at
        # memberguide.gpo.gov for the high-resolution file.
        for bioguide_id, photo_file in regex1.findall(response):
            # this part is added by Congress.gov:
            photo_file = photo_file.replace("_200.jpg", ".jpg")
            if photo_file == bioguide_id.lower() + ".jpg":
                continue  # not a file sourced from GPO
            yield (bioguide_id, photo_file)

        m = regex2.search(response)
        if m:
            # fetch next page of results
            page += 1
            continue
        else:
            # this was the last page (no Next link)
            break

        last_request_time = pause(last_request_time, delay)


def save_metadata(bioguide_id):
    outdir = "congress/metadata"
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    outfile = os.path.join(outdir, bioguide_id + ".yaml")
    with open(outfile, "w") as f:
        f.write("name: GPO Member Guide\n")
        f.write("link: https://memberguide.gpo.gov\n")


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

    for bioguide_id, photo_filename in photo_list:
        photo_url = "https://memberguide.gpo.gov/PictorialImages/" + photo_filename
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
                save_metadata(bioguide_id)
                ok += 1

    print("Downloaded", ok, "member photos.")
    return ok


def resize_photos():
    # Assumes they're congress/original/*.jpg
    os.system(os.path.join("scripts", "resize-photos.sh"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scrape https://memberguide.gpo.gov and save "
        "members' photos named after their Bioguide IDs",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-n",
        "--congress",
        default="114",
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
        "-t",
        "--test",
        action="store_true",
        help="Test mode: don't actually save images",
    )
    args = parser.parse_args()

    br = mechanicalsoup.Browser()
    br.set_user_agent(USER_AGENT)

    photo_list = get_photo_list(br, args.congress, args.delay)

    number = download_photos(br, photo_list, args.outdir, args.delay)

    if number:
        resize_photos()

# End of file
