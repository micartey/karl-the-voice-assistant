#!/bin/bash

# Directory containing the source files
src_dir="src"

# File to store the used dependencies
requirements_file="requirements.txt"

# Remove the requirements file if it exists
rm -rf "$requirements_file"

# Loop through each line in pip freeze
while IFS= read -r line
do
    # Extract the package name (before ==) and use the part after the last '-' if it exists
    pkg_name=$(echo "$line" | cut -d'=' -f1 | awk -F'-' '{print $NF}')

    # Search for the package name in files within src, excluding __* directories
    if grep -qr --exclude-dir="__*" "$pkg_name" "$src_dir"; then
        # If the package is found, append it to the requirements file
        echo "$line" >> "$requirements_file"
    fi
done < <(pip freeze)
