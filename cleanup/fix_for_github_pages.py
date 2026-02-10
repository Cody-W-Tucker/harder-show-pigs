#!/usr/bin/env python3
"""
Final GitHub Pages Cleanup Script
==================================

Fixes URLs and removes WordPress-specific code from HTML files.

Usage:
    python3 fix_for_github_pages.py
"""

import re
from pathlib import Path
import shutil


def fix_broken_css_syntax(html_content):
    """Fix the broken CSS syntax where --general-bg-image is malformed."""
    # Fix: url("./" /index.html") -> url("./")
    html_content = re.sub(
        r'--general-bg-image:\s*url\("\.\/"\s*\/index\.html"\)',
        '--general-bg-image: url("./")',
        html_content
    )
    return html_content


def fix_hardcoded_urls(html_content, file_path):
    """Replace hardcoded URLs with relative paths."""
    src_dir = Path("/home/codyt/Projects/harder/src")
    file_dir = file_path.parent
    
    # Calculate relative path from the HTML file to the root
    relative_to_root = ""
    try:
        depth = len(file_dir.relative_to(src_dir).parts)
        if depth > 0:
            relative_to_root = "../" * depth
    except ValueError:
        pass
    
    # Replace http://dev.hardershowpigs.com/wp-content/ with relative path
    # Use different replacement based on file depth
    html_content = re.sub(
        r'https?://dev\.hardershowpigs\.com/wp-content/',
        f'{relative_to_root}wp-content/',
        html_content
    )
    html_content = re.sub(
        r'https?://hardershowpigs\.com/wp-content/',
        f'{relative_to_root}wp-content/',
        html_content
    )
    
    return html_content


def remove_wordpress_code(html_content):
    """Remove WordPress-specific code from HTML content."""
    removals = []

    # Remove pingback link
    if re.search(r'<link[^>]*rel="pingback"[^>]*>', html_content):
        html_content = re.sub(
            r'\s*<link[^>]*rel="pingback"[^>]*>\s*', "\n", html_content
        )
        removals.append("pingback link")

    # Remove profile link (XFN)
    if re.search(r'<link[^>]*rel="profile"[^>]*>', html_content):
        html_content = re.sub(
            r'\s*<link[^>]*rel="profile"[^>]*>\s*', "\n", html_content
        )
        removals.append("XFN profile link")

    # Remove RSS/Atom feed links
    if re.search(r'type="application/rss\+xml"', html_content):
        html_content = re.sub(
            r'\s*<link\s+[^>]*type="application/rss\+xml"[^>]*>\s*',
            "\n",
            html_content,
            flags=re.IGNORECASE,
        )
        removals.append("RSS feed links")

    # Remove WordPress emoji script
    emoji_patterns = [
        r"<script[^>]*>\s*/\*\s*<!\[CDATA\[\s*\*/\s*window\._wpemojiSettings[\s\S]*?/\*\s*\]\]>\s*\*/\s*</script>",
        r"<script[^>]*>[\s\S]*?window\._wpemojiSettings[\s\S]*?</script>",
    ]
    for pattern in emoji_patterns:
        if re.search(pattern, html_content, re.IGNORECASE):
            html_content = re.sub(pattern, "", html_content, flags=re.IGNORECASE)
            removals.append("WordPress emoji script")
            break

    # Remove WordPress emoji styles
    if '<style id="wp-emoji-styles-inline-css"' in html_content:
        html_content = re.sub(
            r'<style id="wp-emoji-styles-inline-css"[^>]*>[\s\S]*?</style>',
            "",
            html_content,
        )
        removals.append("emoji styles")

    # Remove WordPress block library CSS
    if "wp-block-library-css" in html_content:
        html_content = re.sub(
            r'\s*<link[^>]*id="wp-block-library-css"[^>]*>\s*', "\n", html_content
        )
        removals.append("block library CSS")

    # Remove classic theme styles inline CSS
    if '<style id="classic-theme-styles-inline-css"' in html_content:
        html_content = re.sub(
            r'<style id="classic-theme-styles-inline-css"[^>]*>[\s\S]*?</style>',
            "",
            html_content,
        )
        removals.append("classic theme styles")

    # Remove global styles inline CSS
    if '<style id="global-styles-inline-css"' in html_content:
        html_content = re.sub(
            r'<style id="global-styles-inline-css"[^>]*>[\s\S]*?</style>',
            "",
            html_content,
        )
        removals.append("global styles CSS (~400 lines)")

    # Remove Contact Form 7 CSS
    if "contact-form-7-css" in html_content:
        html_content = re.sub(
            r'\s*<link[^>]*id="contact-form-7-css"[^>]*>\s*', "\n", html_content
        )
        removals.append("Contact Form 7 CSS")

    # Remove admin-ajax variable script
    if "ajax_var" in html_content:
        ajax_pattern = r"<script[^>]*>\s*/\*\s*<!\[CDATA\[\s*\*/\s*var ajax_var\s*=\s*\{[^}]+\};\s*/\*\s*\]\]>\s*\*/\s*</script>"
        html_content = re.sub(ajax_pattern, "", html_content, flags=re.IGNORECASE)
        removals.append("admin-ajax variables")

    # Remove WordPress REST API links
    if "api.w.org" in html_content:
        html_content = re.sub(
            r'\s*<link[^>]*rel="https://api\.w\.org/"[^>]*>\s*', "\n", html_content
        )
        removals.append("REST API links")

    # Remove JSON API links
    if "application/json" in html_content:
        html_content = re.sub(
            r'\s*<link\s+[^>]*type="application/json"[^>]*>\s*', "\n", html_content
        )
        removals.append("JSON API links")

    # Remove EditURI/RSD link
    if "EditURI" in html_content:
        html_content = re.sub(
            r'\s*<link\s+[^>]*rel="EditURI"[^>]*>\s*', "\n", html_content
        )
        removals.append("RSD/EditURI link")

    # Remove WordPress generator meta tag
    if "WordPress" in html_content:
        html_content = re.sub(
            r'\s*<meta[^>]*name="generator"[^>]*content="WordPress[^"]*"[^>]*/?>\s*',
            "\n",
            html_content,
        )
        removals.append("WordPress generator meta")

    # Remove Redux generator meta tag
    if "Redux" in html_content:
        html_content = re.sub(
            r'\s*<meta[^>]*name="generator"[^>]*content="Redux[^"]*"[^>]*/?>\s*',
            "\n",
            html_content,
        )
        removals.append("Redux generator meta")

    # Remove WPBakery generator meta tag
    if "WPBakery" in html_content:
        html_content = re.sub(
            r'\s*<meta[^>]*name="generator"[^>]*content="Powered by WPBakery[^"]*"[^>]*/?>\s*',
            "\n",
            html_content,
        )
        removals.append("WPBakery generator meta")

    # Remove Slider Revolution generator meta tag
    if "Slider Revolution" in html_content:
        html_content = re.sub(
            r'\s*<meta[^>]*name="generator"[^>]*content="Powered by Slider Revolution[^"]*"[^>]*/?>\s*',
            "\n",
            html_content,
        )
        removals.append("Slider Revolution generator meta")

    # Remove shortlink
    if "shortlink" in html_content:
        html_content = re.sub(
            r'\s*<link[^>]*rel="shortlink"[^>]*>\s*', "\n", html_content
        )
        removals.append("shortlink")

    # Remove oEmbed links
    if "oembed" in html_content.lower():
        html_content = re.sub(
            r'\s*<link\s+[^>]*type="application/json\+oembed"[^>]*>\s*',
            "\n",
            html_content,
        )
        html_content = re.sub(
            r'\s*<link\s+[^>]*type="text/xml\+oembed"[^>]*>\s*', "\n", html_content
        )
        removals.append("oEmbed links")

    # Remove Google Maps callback function
    if "rgmkInitGoogleMaps" in html_content:
        html_content = re.sub(
            r"<script[^>]*>\s*function rgmkInitGoogleMaps\(\)[\s\S]*?</script>",
            "",
            html_content,
        )
        removals.append("Google Maps callback")

    # Remove Contact Form 7 scripts
    cf7_scripts = [
        (r'\s*<script[^>]*src="[^"]*contact-form-7[^"]*"[^>]*>\s*</script>\s*', "Contact Form 7 JS"),
        (r'\s*<script[^>]*id="swv-js"[^>]*>\s*</script>\s*', "SWV script"),
        (r'\s*<script[^>]*id="contact-form-7-js[^"]*"[^>]*>[\s\S]*?</script>\s*', "Contact Form 7 inline config"),
    ]
    for pattern, name in cf7_scripts:
        if re.search(pattern, html_content, re.IGNORECASE):
            html_content = re.sub(pattern, "\n", html_content, flags=re.IGNORECASE)
            removals.append(name)

    # Remove WordPress comment reply script
    if "comment-reply" in html_content:
        html_content = re.sub(
            r'\s*<script[^>]*id="comment-reply-js"[^>]*>\s*</script>\s*',
            "\n",
            html_content,
            flags=re.IGNORECASE,
        )
        removals.append("Comment reply script")

    # Remove WordPress polyfill
    if "wp-polyfill" in html_content:
        html_content = re.sub(
            r'\s*<script[^>]*id="wp-polyfill-js"[^>]*>\s*</script>\s*',
            "\n",
            html_content,
            flags=re.IGNORECASE,
        )
        removals.append("WP polyfill")

    # Remove foodfarm-params with admin-ajax URLs
    if 'foodfarm_params' in html_content or 'admin-ajax.php' in html_content:
        ajax_pattern = r'<script[^>]*id="foodfarm-script-js-extra"[^>]*>\s*/\*\s*<!\[CDATA\[\s*\*/\s*var foodfarm_params\s*=\s*\{[\s\S]*?\};\s*/\*\s*\]\]>\s*\*/\s*</script>'
        if re.search(ajax_pattern, html_content, re.IGNORECASE):
            html_content = re.sub(ajax_pattern, "", html_content, flags=re.IGNORECASE)
            removals.append("Foodfarm ajax params")

    # Remove other admin-ajax variable scripts
    if "admin-ajax.php" in html_content:
        generic_ajax_pattern = r'<script[^>]*>[^<]*admin-ajax\.php[^<]*</script>'
        if re.search(generic_ajax_pattern, html_content, re.IGNORECASE):
            html_content = re.sub(generic_ajax_pattern, "", html_content, flags=re.IGNORECASE)
            removals.append("admin-ajax variables")

    # Remove wpcf7 form hidden fields
    if "_wpcf7" in html_content:
        wpcf7_pattern = r'<div style="display:\s*none">\s*<input[^>]*name="_wpcf7"[^>]*/?>\s*<input[^>]*name="_wpcf7_version"[^>]*/?>\s*<input[^>]*name="_wpcf7_locale"[^>]*/?>\s*<input[^>]*name="_wpcf7_unit_tag"[^>]*/?>\s*<input[^>]*name="_wpcf7_container_post"[^>]*/?>\s*<input[^>]*name="_wpcf7_posted_data_hash"[^>]*/?>\s*</div>'
        if re.search(wpcf7_pattern, html_content, re.IGNORECASE | re.DOTALL):
            html_content = re.sub(wpcf7_pattern, "", html_content, flags=re.IGNORECASE | re.DOTALL)
            removals.append("WPCF7 hidden fields")

    # Remove WordPress form action URLs
    if 'simply_static_page=' in html_content:
        html_content = re.sub(
            r'action="[^"]*\?simply_static_page=\d+#wpcf7-f\d+-p\d+-o\d+"',
            'action="#"',
            html_content
        )
        removals.append("WP form actions")

    # Remove unused time-circles.js
    if 'time-circles' in html_content:
        html_content = re.sub(
            r'\s*<script[^>]*src="[^"]*time-circles[^"]*"[^>]*>\s*</script>\s*',
            '\n',
            html_content,
            flags=re.IGNORECASE
        )
        removals.append("time-circles.js (unused)")

    # Remove unused prettyPhoto CSS and JS
    if 'prettyPhoto' in html_content:
        html_content = re.sub(
            r'\s*<link[^>]*href="[^"]*prettyPhoto[^"]*"[^>]*>\s*',
            '\n',
            html_content,
            flags=re.IGNORECASE
        )
        html_content = re.sub(
            r'\s*<script[^>]*src="[^"]*prettyPhoto[^"]*"[^>]*>\s*</script>\s*',
            '\n',
            html_content,
            flags=re.IGNORECASE
        )
        removals.append("prettyPhoto (unused)")

    # Remove object-cache-pro HTML comments
    if 'object-cache-pro' in html_content:
        html_content = re.sub(
            r'\s*<!--\s*plugin=object-cache-pro[^>]*-->\s*',
            '\n',
            html_content,
            flags=re.IGNORECASE
        )
        removals.append("object-cache-pro comment")

    # Clean up multiple consecutive blank lines
    html_content = re.sub(r"\n{3,}", "\n\n", html_content)

    return html_content, removals


def process_html_file(file_path):
    """Process a single HTML file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_length = len(content)
        
        # Step 1: Fix broken CSS syntax
        content = fix_broken_css_syntax(content)
        
        # Step 2: Fix hardcoded URLs
        content = fix_hardcoded_urls(content, file_path)
        
        # Step 3: Remove WordPress code
        content, removals = remove_wordpress_code(content)
        
        new_length = len(content)

        if original_length != new_length:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return {
                "file": str(file_path),
                "bytes_removed": original_length - new_length,
                "removals": removals,
            }
        else:
            return None

    except Exception as e:
        print(f"  ✗ Error processing {file_path}: {e}")
        return None


def delete_unreferenced_files():
    """Delete files listed in unreferenced_files.txt."""
    # Get the script's directory and look for unreferenced_files.txt in cleanup dir
    script_dir = Path(__file__).parent
    unreferenced_file = script_dir / "unreferenced_files.txt"
    project_root = script_dir.parent
    
    if not unreferenced_file.exists():
        return []
    
    deleted = []
    with open(unreferenced_file, "r") as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            file_path = project_root / line
            if file_path.exists():
                try:
                    if file_path.is_file():
                        file_path.unlink()
                        deleted.append(str(file_path.relative_to(project_root)))
                    elif file_path.is_dir():
                        shutil.rmtree(file_path)
                        deleted.append(str(file_path.relative_to(project_root)) + " (dir)")
                except Exception as e:
                    print(f"  ✗ Error deleting {file_path}: {e}")
    
    return deleted


def main():
    """Main function to process all HTML files and cleanup."""
    # Get the script's directory and project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    src_dir = project_root / "src"

    if not src_dir.exists():
        print(f"Error: Directory {src_dir} does not exist")
        return

    print("=" * 70)
    print("GITHUB PAGES CLEANUP SCRIPT")
    print("=" * 70)
    
    # Step 1: Delete unreferenced files
    print("\n[1/3] Deleting unreferenced files...")
    deleted_files = delete_unreferenced_files()
    if deleted_files:
        for f in deleted_files:
            print(f"  ✓ Deleted: {f}")
        print(f"\n  Deleted {len(deleted_files)} items")
    else:
        print("  - No unreferenced files to delete")

    # Step 2: Process HTML files
    print("\n[2/3] Processing HTML files...")
    html_files = list(src_dir.rglob("*.html"))
    print(f"  Found {len(html_files)} HTML files\n")

    modified_files = []
    for i, html_file in enumerate(html_files, 1):
        print(f"  [{i}/{len(html_files)}] {html_file.relative_to(src_dir)}", end=" ")
        result = process_html_file(html_file)
        if result:
            modified_files.append(result)
            print(f"✓ (-{result['bytes_removed']:,} bytes)")
        else:
            print("- (no changes)")

    # Step 3: Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Files deleted: {len(deleted_files)}")
    print(f"HTML files processed: {len(html_files)}")
    print(f"HTML files modified: {len(modified_files)}")

    if modified_files:
        total_bytes = sum(f["bytes_removed"] for f in modified_files)
        print(f"Total bytes removed from HTML: {total_bytes:,}")
        
        # Show unique removals
        all_removals = set()
        for f in modified_files:
            all_removals.update(f["removals"])
        if all_removals:
            print("\nCleanup items found:")
            for item in sorted(all_removals):
                print(f"  - {item}")

    print("\n✓ Cleanup complete! Site is ready for GitHub Pages.")
    print("\nNext steps:")
    print("  1. Commit changes: git add -A && git commit -m 'Prepare for GitHub Pages'")
    print("  2. Push to GitHub")
    print("  3. Enable GitHub Pages in repo settings")
    print("  4. Set source to 'main' branch and folder to '/src'")


if __name__ == "__main__":
    main()
