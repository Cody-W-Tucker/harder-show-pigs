#!/usr/bin/env python3
"""
Site Update Script for Harder Show Pigs
Updates content across all HTML files in src/ directory
"""

import re
import argparse
from pathlib import Path
from typing import List, Optional

# Configuration
SRC_DIR = Path("/home/codyt/Projects/harder/src")

# List of all HTML files to update
HTML_FILES = [
    "index.html",
    "about/index.html",
    "our-boars/index.html",
    "previous-winning/index.html",
    "our-gallery/index.html",
    "contact/index.html",
]


def get_all_html_files() -> List[Path]:
    """Get all HTML files in src directory"""
    files = []
    for html_file in HTML_FILES:
        full_path = SRC_DIR / html_file
        if full_path.exists():
            files.append(full_path)
        else:
            print(f"Warning: {full_path} not found")
    return files


def read_file(file_path: Path) -> str:
    """Read file content"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(file_path: Path, content: str) -> None:
    """Write content to file"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


def search_replace(files: List[Path], search: str, replace: str, dry_run: bool = True) -> dict:
    """
    Perform search and replace across all files
    Returns dict with file paths and match counts
    """
    results = {}
    
    for file_path in files:
        content = read_file(file_path)
        matches = content.count(search)
        
        if matches > 0:
            results[str(file_path)] = matches
            
            if not dry_run:
                new_content = content.replace(search, replace)
                write_file(file_path, new_content)
                print(f"  Updated: {file_path} ({matches} replacements)")
            else:
                print(f"  Would update: {file_path} ({matches} replacements)")
    
    return results


def update_footer_copyright(year: str, dry_run: bool = True) -> dict:
    """Update copyright year in footer"""
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Updating copyright year to {year}...")
    
    files = get_all_html_files()
    old_pattern = r'Copyright © \d{4} HarderShowPigs'
    new_text = f'Copyright © {year} HarderShowPigs'
    
    results = {}
    
    for file_path in files:
        content = read_file(file_path)
        matches = len(re.findall(old_pattern, content))
        
        if matches > 0:
            results[str(file_path)] = matches
            
            if not dry_run:
                new_content = re.sub(old_pattern, new_text, content)
                write_file(file_path, new_content)
                print(f"  Updated: {file_path}")
            else:
                print(f"  Would update: {file_path}")
    
    return results


def update_contact_info(field: str, new_value: str, dry_run: bool = True) -> dict:
    """
    Update contact information
    Fields: phone, email, address
    """
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Updating {field} to {new_value}...")
    
    files = get_all_html_files()
    results = {}
    
    if field == 'phone':
        search_pattern = r'href="callto:\d+"[^>]*>\+?1?[^<]*\(?\d{3}\)?[^\d]?\d{3}[^\d]?\d{4}'
        clean_number = new_value.replace("-", "").replace(" ", "")
        replace_text = f'href="callto:{clean_number}">+1 {new_value}'
    elif field == 'email':
        search_pattern = r'href="mailto:[^"]+"[^>]*>[^<]+'
        replace_text = f'href="mailto:{new_value}">{new_value}'
    elif field == 'address':
        search_pattern = r'<span>\s*\d+[^<]+</span>\s*</li>\s*<li>\s*<i class="fa fa-map-marker"></i>'
        replace_text = f'<span>{new_value}</span>'
    else:
        print(f"Unknown field: {field}")
        return results
    
    for file_path in files:
        content = read_file(file_path)
        matches = len(re.findall(search_pattern, content))
        
        if matches > 0:
            results[str(file_path)] = matches
            
            if not dry_run:
                new_content = re.sub(search_pattern, replace_text, content)
                write_file(file_path, new_content)
                print(f"  Updated: {file_path}")
            else:
                print(f"  Would update: {file_path}")
    
    return results


def find_pattern(pattern: str, files: Optional[List[Path]] = None) -> dict:
    """Find a pattern across all files"""
    if files is None:
        files = get_all_html_files()
    
    print(f"\nSearching for pattern: {pattern}")
    results = {}
    
    for file_path in files:
        content = read_file(file_path)
        matches = re.findall(pattern, content)
        if matches:
            results[str(file_path)] = matches
            print(f"  Found in {file_path}: {len(matches)} matches")
            for i, match in enumerate(matches[:3], 1):
                preview = match[:80] + "..." if len(match) > 80 else match
                print(f"    {i}. {preview}")
    
    return results


def update_facebook_url(new_url: str, dry_run: bool = True) -> dict:
    """Update Facebook link across all files"""
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Updating Facebook URL...")
    
    files = get_all_html_files()
    old_pattern = r'href="https://www\.facebook\.com/[^"]+"'
    
    results = {}
    
    for file_path in files:
        content = read_file(file_path)
        matches = len(re.findall(old_pattern, content))
        
        if matches > 0:
            results[str(file_path)] = matches
            
            if not dry_run:
                new_content = re.sub(old_pattern, f'href="{new_url}"', content)
                write_file(file_path, new_content)
                print(f"  Updated: {file_path}")
            else:
                print(f"  Would update: {file_path}")
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Update HTML files across the site",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search for text (dry run by default)
  python update_site.py --search "2024" --replace "2025"
  
  # Actually apply the changes
  python update_site.py --search "2024" --replace "2025" --apply
  
  # Update copyright year
  python update_site.py --copyright 2025 --apply
  
  # Update contact info
  python update_site.py --contact phone --value "308-872-5611" --apply
  
  # Find pattern
  python update_site.py --find "facebook\\.com"
  
  # Update Facebook URL
  python update_site.py --facebook "https://facebook.com/newurl" --apply
        """
    )
    
    parser.add_argument('--search', '-s', help='Text to search for')
    parser.add_argument('--replace', '-r', help='Text to replace with')
    parser.add_argument('--apply', '-a', action='store_true', help='Apply changes (default is dry-run)')
    parser.add_argument('--copyright', '-c', help='Update copyright year')
    parser.add_argument('--contact', choices=['phone', 'email', 'address'], help='Contact field to update')
    parser.add_argument('--value', '-v', help='New value for contact field')
    parser.add_argument('--find', '-f', help='Find pattern (regex)')
    parser.add_argument('--facebook', help='Update Facebook URL')
    
    args = parser.parse_args()
    
    if args.find:
        find_pattern(args.find)
        return
    
    if args.copyright:
        results = update_footer_copyright(args.copyright, dry_run=not args.apply)
        print(f"\nFound {len(results)} files with copyright text")
        if not args.apply:
            print("Use --apply to make these changes")
        return
    
    if args.contact and args.value:
        results = update_contact_info(args.contact, args.value, dry_run=not args.apply)
        print(f"\nFound {len(results)} files with {args.contact} info")
        if not args.apply:
            print("Use --apply to make these changes")
        return
    
    if args.facebook:
        results = update_facebook_url(args.facebook, dry_run=not args.apply)
        print(f"\nFound {len(results)} files with Facebook links")
        if not args.apply:
            print("Use --apply to make these changes")
        return
    
    if args.search and args.replace:
        files = get_all_html_files()
        results = search_replace(files, args.search, args.replace, dry_run=not args.apply)
        print(f"\nFound {len(results)} files with matches")
        if not args.apply:
            print("Use --apply to make these changes")
        return
    
    # No arguments provided
    parser.print_help()
    print("\n\nCommon use cases:")
    print("  1. Update copyright year:  python update_site.py --copyright 2025 --apply")
    print("  2. Search and replace:     python update_site.py --search 'old' --replace 'new' --apply")
    print("  3. Find text:              python update_site.py --find 'pattern'")
    print("  4. Update phone:           python update_site.py --contact phone --value '308-872-5611' --apply")


if __name__ == "__main__":
    main()
