# Usage: scripts/update_image.sh url bioguide_id issue_number
# Example: scripts/update_image.sh https://cloud.githubusercontent.com/assets/3171982/7505422/46c2791e-f420-11e4-9360-0bb6ff136a04.jpg T000476 85

# Download an original image, delete and create new thumbnails,
# open its metadata file for editing, do some git things.

echo "URL:" $1
echo "Bioguide ID:" $2
echo "Issue number:" $3
echo "name: "    > congress/metadata/$2.yaml
echo "link: $1" >> congress/metadata/$2.yaml
bbedit congress/metadata/$2.yaml
wget $1 -O congress/original/$2.jpg
rm congress/225x275/$2.jpg
rm congress/450x550/$2.jpg
scripts/resize-photos.sh
git status
git add congress
git status
echo git commit -m \"Update $2 via \#$3\"
