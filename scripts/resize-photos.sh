#!/bin/sh

# Script to resize congress photos into the sizes we typically use.
# Run this from a directory with photos in it, named by bioguide ID.
# The photos will be resized and placed into directories named after the size, retaining their original filename.

BASEDIR=congress

for SIZE in "40x50" "100x125" "200x250"
    do
    mkdir $BASEDIR/$SIZE;
    for f in $BASEDIR/original/*.jpg
    do
        f=$(basename "$f")
        convert $BASEDIR/original/$f -resize $SIZE^ -gravity center -extent $SIZE $BASEDIR/$SIZE/$f;
    done
done
