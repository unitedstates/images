## US Images

Images of members of the US Congress.


## Using the photos

Photos are available at predictable URLs, by size and Bioguide ID. Photos are served using Github Pages.

```
http://theunitedstates.io/images/congress/[size]/[bioguide].jpg
```

`[size]` can be one of:

* `original` - As originally downloaded. Typically, `589x719`, but no guarantees are made.
* `200x250`
* `100x125`
* `40x50`

`[bioguide]` must be a Bioguide ID. These are unique IDs for members of Congress, as defined by the [Congressional Bioguide](http://bioguide.congress.gov). They can be found and connected many other Congressional datasets, including the partner dataset over at [unitedstates/congress-legislators](https://github.com/unitedstates/congress-legislators).


## Gathering more photos

This project uses a Python script that scrapes the [Government Printing Office's Member Guide](http://memberguide.gpo.gov/) for official photos of Members of Congress. You can run the script to find and fetch new

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

In this case, [open a ticket](/unitedstates/images/issues/new), and include:

* The name and Bioguide ID of the member of Congress.
* A link to the image you're suggesting we incorporate, and to a page that displays that image.
* Why you believe the image is definitely official and in the public domain.


## Public domain

The photos of members of Congress are from the Government Printing Office, which [has assured Public Knowledge's Michael Weinberg that all photos are public domain](https://github.com/sunlightlabs/congress/issues/432#issuecomment-34481338).

All other files in this project are [dedicated to the public domain](LICENSE). As spelled out in [CONTRIBUTING](CONTRIBUTING.md):

> The project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](http://creativecommons.org/publicdomain/zero/1.0/).

> All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.
