#!/usr/bin/env python3
"""
Update year references in the website HTML.

Updates image paths and srcset attributes to reference a new year's letter images.
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple

# Configuration
SRC_DIR = Path("/home/codyt/Projects/harder/src")
INDEX_FILE = SRC_DIR / "index.html"


def parse_srcset(srcset: str) -> List[Tuple[str, str]]:
    """
    Parse a srcset attribute into list of (url, descriptor) tuples.
    
    Example:
        "image.jpg 1275w, image-791.jpg 791w" 
        -> [("image.jpg", "1275w"), ("image-791.jpg", "791w")]
    """
    images = []
    parts = [p.strip() for p in srcset.split(",")]
    for part in parts:
        match = re.match(r'(.+?)\s+(\d+w)$', part)
        if match:
            images.append((match.group(1), match.group(2)))
        else:
            # No descriptor (shouldn't happen but handle it)
            images.append((part, ""))
    return images


def update_srcset(srcset: str, from_year: int, to_year: int) -> str:
    """Update year in srcset attribute."""
    images = parse_srcset(srcset)
    new_parts = []
    for url, descriptor in images:
        new_url = url.replace(f"/uploads/{from_year}/", f"/uploads/{to_year}/")
        if descriptor:
            new_parts.append(f"{new_url} {descriptor}")
        else:
            new_parts.append(new_url)
    return ", ".join(new_parts)


def update_image_references(
    html_content: str,
    from_year: int,
    to_year: int
) -> str:
    """
    Update all image references from one year to another.
    
    Args:
        html_content: The HTML content to update
        from_year: Current year in the HTML
        to_year: New year to update to
    
    Returns:
        Updated HTML content
    """
    # Pattern to match img tags
    img_pattern = r'(<img[^>]*?)src="([^"]*?)"([^>]*?)>'
    
    def replace_img(match):
        before = match.group(1)
        src = match.group(2)
        after = match.group(3)
        
        # Update src
        new_src = src.replace(f"/uploads/{from_year}/", f"/uploads/{to_year}/")
        
        # Update srcset if present
        srcset_match = re.search(r'srcset="([^"]*)"', after)
        if srcset_match:
            old_srcset = srcset_match.group(1)
            new_srcset = update_srcset(old_srcset, from_year, to_year)
            after = after.replace(f'srcset="{old_srcset}"', f'srcset="{new_srcset}"')
        
        return f'{before}src="{new_src}"{after}>'
    
    updated_content = re.sub(img_pattern, replace_img, html_content)
    
    # Also update anchor hrefs that point to images
    anchor_pattern = r'(<a[^>]*?)href="([^"]*?uploads/\d{4}/[^"]*?)"([^>]*?)>'
    
    def replace_anchor(match):
        before = match.group(1)
        href = match.group(2)
        after = match.group(3)
        
        new_href = href.replace(f"/uploads/{from_year}/", f"/uploads/{to_year}/")
        return f'{before}href="{new_href}"{after}>'
    
    updated_content = re.sub(anchor_pattern, replace_anchor, updated_content)
    
    return updated_content


def update_year_references(
    html_content: str,
    from_year: int,
    to_year: int,
    dry_run: bool = True
) -> Tuple[str, int]:
    """
    Update all year references in HTML content.
    
    Returns:
        Tuple of (updated content, number of changes)
    """
    original = html_content
    updated = update_image_references(html_content, from_year, to_year)
    
    # Count changes
    changes = 0
    if original != updated:
        # Simple line-by-line comparison
        orig_lines = original.split("\n")
        new_lines = updated.split("\n")
        for orig, new in zip(orig_lines, new_lines):
            if orig != new:
                changes += 1
    
    return updated, changes


def main():
    parser = argparse.ArgumentParser(
        description="Update year references in website HTML.",
        epilog="""
Examples:
  # Dry run - preview what would change
  python3 update_year.py --from 2025 --to 2026
  
  # Actually update the HTML
  python3 update_year.py --from 2025 --to 2026 --apply
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--from",
        dest="from_year",
        type=int,
        required=True,
        help="Current year in the HTML (e.g., 2025)"
    )
    
    parser.add_argument(
        "--to",
        dest="to_year",
        type=int,
        required=True,
        help="New year to update to (e.g., 2026)"
    )
    
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually update the files (default is dry-run)"
    )
    
    parser.add_argument(
        "--file",
        type=Path,
        default=INDEX_FILE,
        help=f"HTML file to update (default: {INDEX_FILE})"
    )
    
    args = parser.parse_args()
    
    # Read the HTML file
    if not args.file.exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Update the content
    updated_content, changes = update_year_references(
        content,
        args.from_year,
        args.to_year,
        dry_run=not args.apply
    )
    
    if changes == 0:
        print(f"No changes needed - no references to {args.from_year} found")
        return
    
    # Show diff-like output
    print(f"\nFound {changes} lines to update:")
    print("-" * 60)
    
    orig_lines = content.split("\n")
    new_lines = updated_content.split("\n")
    
    for i, (orig, new) in enumerate(zip(orig_lines, new_lines), 1):
        if orig != new:
            print(f"\nLine {i}:")
            print(f"  - {orig[:100]}{'...' if len(orig) > 100 else ''}")
            print(f"  + {new[:100]}{'...' if len(new) > 100 else ''}")
    
    if args.apply:
        try:
            with open(args.file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"\n{'='*60}")
            print(f"Successfully updated {args.file}")
            print(f"Changed {changes} lines from {args.from_year} to {args.to_year}")
            print(f"{'='*60}")
        except Exception as e:
            print(f"\nError writing file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"\n{'='*60}")
        print("DRY RUN - No files were modified")
        print(f"Run with --apply to make these changes")
        print(f"{'='*60}")


if __name__ == "__main__":
    main()
