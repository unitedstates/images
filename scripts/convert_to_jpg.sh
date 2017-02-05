#!/bin/bash

# The scripts finds all files that don't end with .jpg and either renames them or
# converts them to jpg.

# Find all the files!
files=$(find congress/original/ -not -name '*.jpg' -not -type d)

for file in $files; do
    fileext=${file##*.} # Get the file extension
    filename=${file%.*} # Get the file name with path and without extension

    if [ "$fileext" = "jpeg" ]; then
        mv $file $filename.jpg # Move because jpeg and jpg are basically the same
    else
        convert $file $filename.jpg # Convert to a jpg
        rm $file
    fi
done
