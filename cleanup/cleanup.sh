#!/usr/bin/env bash

# Script to delete files listed in unreferenced_files.txt

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Check if the file exists
if [ ! -f "$SCRIPT_DIR/unreferenced_files.txt" ]; then
    echo "Error: unreferenced_files.txt not found. Run find_unreferenced_wp_files.sh first."
    exit 1
fi

# Confirm deletion
echo "This will delete all files listed in unreferenced_files.txt. Are you sure? (y/N)"
read -r response
if [[ ! "$response" =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
fi

# Delete files (paths are relative to project root)
while IFS= read -r file; do
    # Skip empty lines and comments
    [[ -z "$file" || "$file" =~ ^[[:space:]]*# ]] && continue
    
    full_path="$PROJECT_ROOT/$file"
    if [ -f "$full_path" ]; then
        rm -f "$full_path"
        echo "Deleted: $file"
    else
        echo "Not found: $file"
    fi
done < "$SCRIPT_DIR/unreferenced_files.txt"

echo "Cleanup complete."