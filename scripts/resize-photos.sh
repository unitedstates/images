#!/bin/sh

# Script to resize congress photos into the sizes we typically use.
# Run this from the root images directory: scripts/resize-photos.sh.
# Directory congress/original contains images named by bioguide ID.
# The photos will be resized and placed into directories named after the size, retaining their original filename.

BASEDIR=congress

for SIZE in "225x275" "450x550"
    do
    mkdir $BASEDIR/$SIZE;
    for f in $BASEDIR/original/*.jpg
    do
        f=$(basename "$f")
        outfile=$BASEDIR/$SIZE/$f
        if [ ! -f $outfile ]; then
            convert $BASEDIR/original/$f -resize $SIZE^ -gravity center -extent $SIZE $outfile;
        fi
    done
done
