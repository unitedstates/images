# Usage: scripts/update_image.sh url bioguide_id
# Example: scripts/update_image.sh https://cloud.githubusercontent.com/assets/3171982/7097441/ab606912-dfa3-11e4-8e1f-bb7c944fe877.jpg Y000066

# Download an original image, delete and create new thumbnails,
# open its metadata file for editing, do some git things.

echo "URL:" $1
echo "Bioguide ID:" $2
edit congress/metadata/$2.yaml
wget $1 -O congress/original/$2.jpg
rm congress/225x275/$2.jpg
rm congress/450x550/$2.jpg
scripts/resize-photos.sh
git status
git add congress
git status
echo git commit -m \"Update $2 via \#
