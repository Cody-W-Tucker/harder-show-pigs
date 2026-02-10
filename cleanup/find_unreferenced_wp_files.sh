#!/usr/bin/env bash

# Script to find files in wp-content and wp-includes not mentioned elsewhere in src/

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Set the base directory (src is at project root)
BASE_DIR="$PROJECT_ROOT/src"

# Output file (in cleanup directory)
OUTPUT_FILE="$SCRIPT_DIR/unreferenced_files.txt"

# Directories to check
WP_DIRS=("$BASE_DIR/wp-content" "$BASE_DIR/wp-includes")

# Function to check if a file is mentioned elsewhere
is_mentioned() {
    local file="$1"
    local basename=$(basename "$file")
    # Search for basename in src/, excluding the file itself
    grep -r "$basename" "$BASE_DIR" | grep -v "$file" > /dev/null 2>&1
    return $?
}

# Function to get path relative to project root
get_relative_path() {
    local full_path="$1"
    echo "${full_path#$PROJECT_ROOT/}"
}

# Clear output file
> "$OUTPUT_FILE"

# Find all files in wp-content and wp-includes
for dir in "${WP_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        find "$dir" -type f | while read -r file; do
            if ! is_mentioned "$file"; then
                # Store path relative to project root
                rel_path=$(get_relative_path "$file")
                echo "$rel_path" >> "$OUTPUT_FILE"
            fi
        done
    fi
done

echo "Unreferenced files list saved to $OUTPUT_FILE"