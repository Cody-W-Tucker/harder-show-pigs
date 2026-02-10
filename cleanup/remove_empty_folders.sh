#!/usr/bin/env bash

# Script to remove empty directories in src/
# Run this after cleanup.sh to remove folders that are now empty

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SRC_DIR="$PROJECT_ROOT/src"

if [ ! -d "$SRC_DIR" ]; then
    echo "Error: $SRC_DIR not found"
    exit 1
fi

echo "Removing empty directories from src/..."
echo ""

# Keep removing empty directories until none are found
deleted_count=0
while true; do
    found_empty=0
    
    # Find empty directories (depth-first to handle nested empty dirs)
    while IFS= read -r -d '' dir; do
        # Check if directory is empty (no files, no subdirectories)
        if [ -z "$(ls -A "$dir" 2>/dev/null)" ]; then
            echo "  Deleting: $(realpath --relative-to="$PROJECT_ROOT" "$dir")"
            rmdir "$dir"
            ((deleted_count++))
            found_empty=1
        fi
    done < <(find "$SRC_DIR" -type d -print0 | sort -rz)
    
    # If no empty directories found in this pass, we're done
    if [ $found_empty -eq 0 ]; then
        break
    fi
done

echo ""
if [ $deleted_count -eq 0 ]; then
    echo "No empty directories found."
else
    echo "Removed $deleted_count empty directorie(s)."
fi
