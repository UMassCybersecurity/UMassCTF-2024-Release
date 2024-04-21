#!/bin/bash

source kctf/activate

base_dir="."

# Find all directories containing 'challenge.yaml' up to two levels deep
find "$base_dir" -maxdepth 3 -type f -name 'challenge.yaml' | while read -r file; do
  dir=$(dirname "$file")
  
  echo "Changing to directory: $dir"
  if cd $dir; then
    if command -v kctf >/dev/null 2>&1; then
      kctf chal start
    else
      echo "kctf command not found"
    fi
  else
    echo "Failed to enter directory: $dir"
  fi

  cd "../../" || { echo "Failed to return to base directory $base_dir"; exit 1; }
done