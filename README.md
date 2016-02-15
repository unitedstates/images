# Images of Congress

Public domain images of members of the US Congress.

## Using the photos

Photos are available at predictable URLs, by size and Bioguide ID. Photos are served using GitHub Pages.

```
https://theunitedstates.io/images/congress/[size]/[bioguide].jpg
```

`[size]` can be one of:

* `original` - As originally downloaded. Typically, `675x825`, but [it can vary](https://github.com/unitedstates/images/issues/1#issuecomment-35070231).
* `450x550`
* `225x275`

`[bioguide]` must be a Bioguide ID. These are unique IDs for members of Congress, as defined by the [Congressional Bioguide](http://bioguide.congress.gov). They can be found and connected to many other Congressional datasets, including the partner dataset over at [unitedstates/congress-legislators](https://github.com/unitedstates/congress-legislators).

**Note:** Our HTTPS permalinks are provided through CloudFlare's [Universal SSL](https://blog.cloudflare.com/introducing-universal-ssl/), which also uses "Flexible SSL" to talk to GitHub Pages' unencrypted endpoints. So, you should know that it's not an end-to-end encrypted channel, but is encrypted between your client use and CloudFlare's servers (which at least should dissociate your requests from client IP addresses).

## Downloading all images of a particular size

If you want to quickly grab all images of a particular size without cloning the entire repo (and have `svn` installed), you can just do something like this:

`svn checkout https://github.com/unitedstates/images/trunk/congress/225x275`

## Gathering more photos

[![Build Status](https://travis-ci.org/unitedstates/images.svg?branch=gh-pages)](https://travis-ci.org/unitedstates/images)
[![Coverage Status](https://coveralls.io/repos/unitedstates/images/badge.svg?branch=gh-pages&service=github)](https://coveralls.io/github/unitedstates/images?branch=gh-pages)

This project uses a Python script that scrapes the [Government Printing Office's Member Guide](http://memberguide.gpo.gov/) for official photos of Members of Congress. You can run the script to find and fetch new photos.

Install dependencies with:

```bash
pip install -r requirements.txt
```

Run the script with:

```bash
./scripts/gpo_member_photos.py
```


## Contributing other photos

If GPO doesn't have a photo for someone in their member guide, we may be willing to accept a photo from another source.

In this case, [open a ticket](https://github.com/unitedstates/images/issues/new), and include:

* The name and Bioguide ID of the member of Congress.
* A link to the image you're suggesting we incorporate, and to a page that displays that image.
* Why you believe the image is definitely official and in the public domain.


## Public domain

The photos of members of Congress are from the Government Printing Office, which [has assured us that all photos are public domain](https://github.com/sunlightlabs/congress/issues/432#issuecomment-34481338).

All other files in this project are [dedicated to the public domain](LICENSE). As spelled out in [CONTRIBUTING](CONTRIBUTING.md):

> The project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](http://creativecommons.org/publicdomain/zero/1.0/).

> All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.
