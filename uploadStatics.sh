#!/bin/bash

# Usage: ./script_name.sh [filter_string]
# Example: ./script_name.sh project1

# Set the name of your Google Cloud Storage bucket
BUCKET_NAME="chal-static"

# Check if a filter string is provided
if [ -z "$1" ]; then
    echo "No filter string provided. Uploading all 'static' directories at the third level."
    # Find all directories named 'static' exactly at the third level
    directories=$(find . -type d -name 'static' | grep -E '^./[^/]*/[^/]*/static$')
else
    echo "Filter string provided: $1. Uploading 'static' directories containing '$1' in the path."
    # Find all directories named 'static' that include the filter string in the path
    directories=$(find . -type d -name 'static' | grep -E "^./[^/]*/[^/]*/static$" | grep "$1")
fi

# Loop through the found directories and upload each
for dir in $directories; do
    # Extract the path without './'
    path_without_dot=$(echo $dir | sed 's|^\./||')
    
    # Full path for the bucket (remove the '/static' part for the bucket structure)
    bucket_path=$(echo $path_without_dot | sed 's|/static||')

    echo "Uploading ${dir} to gs://${BUCKET_NAME}/${bucket_path}/..."
    gsutil -m cp -r "${dir}/" "gs://${BUCKET_NAME}/${bucket_path}/"
done

echo "Upload complete."
