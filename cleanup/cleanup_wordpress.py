#!/usr/bin/env python3
"""
WordPress-to-Static Cleanup Script
====================================

Removes WordPress-specific code from HTML files when converting
a WordPress site to a static HTML site.

Usage:
    python3 cleanup_wordpress.py

The script will recursively find all HTML files in the src/ directory
and remove WordPress-specific code blocks.
"""

import re
from pathlib import Path


def remove_wordpress_code(html_content):
    """Remove WordPress-specific code from HTML content."""

    # Track what we removed for reporting
    removals = []

    # 1. Remove pingback link
    if re.search(r'<link[^>]*rel="pingback"[^>]*>', html_content):
        html_content = re.sub(
            r'\s*<link[^>]*rel="pingback"[^>]*>\s*', "\n", html_content
        )
        removals.append("pingback link")

    # 2. Remove profile link (XFN)
    if re.search(r'<link[^>]*rel="profile"[^>]*>', html_content):
        html_content = re.sub(
            r'\s*<link[^>]*rel="profile"[^>]*>\s*', "\n", html_content
        )
        removals.append("XFN profile link")

    # 3. Remove RSS/Atom feed links
    if re.search(r'type="application/rss\+xml"', html_content):
        html_content = re.sub(
            r'\s*<link\s+[^>]*type="application/rss\+xml"[^>]*>\s*',
            "\n",
            html_content,
            flags=re.IGNORECASE,
        )
        removals.append("RSS feed links")

    # 4. Remove WordPress emoji script - handle various formats
    emoji_patterns = [
        # With CDATA
        r"<script[^>]*>\s*/\*\s*<!\[CDATA\[\s*\*/\s*window\._wpemojiSettings[\s\S]*?/\*\s*\]\]>\s*\*/\s*</script>",
        # Without CDATA
        r"<script[^>]*>[\s\S]*?window\._wpemojiSettings[\s\S]*?</script>",
    ]
    for pattern in emoji_patterns:
        if re.search(pattern, html_content, re.IGNORECASE):
            html_content = re.sub(pattern, "", html_content, flags=re.IGNORECASE)
            removals.append("WordPress emoji script")
            break

    # 5. Remove WordPress emoji styles
    if '<style id="wp-emoji-styles-inline-css"' in html_content:
        html_content = re.sub(
            r'<style id="wp-emoji-styles-inline-css"[^>]*>[\s\S]*?</style>',
            "",
            html_content,
        )
        removals.append("emoji styles")

    # 6. Remove WordPress block library CSS
    if "wp-block-library-css" in html_content:
        html_content = re.sub(
            r'\s*<link[^>]*id="wp-block-library-css"[^>]*>\s*', "\n", html_content
        )
        removals.append("block library CSS")

    # 7. Remove classic theme styles inline CSS
    if '<style id="classic-theme-styles-inline-css"' in html_content:
        html_content = re.sub(
            r'<style id="classic-theme-styles-inline-css"[^>]*>[\s\S]*?</style>',
            "",
            html_content,
        )
        removals.append("classic theme styles")

    # 8. Remove global styles inline CSS (huge block with WP presets)
    if '<style id="global-styles-inline-css"' in html_content:
        html_content = re.sub(
            r'<style id="global-styles-inline-css"[^>]*>[\s\S]*?</style>',
            "",
            html_content,
        )
        removals.append("global styles CSS (~400 lines)")

    # 9. Remove Contact Form 7 CSS
    if "contact-form-7-css" in html_content:
        html_content = re.sub(
            r'\s*<link[^>]*id="contact-form-7-css"[^>]*>\s*', "\n", html_content
        )
        removals.append("Contact Form 7 CSS")

    # 10. Remove admin-ajax variable script
    if "ajax_var" in html_content:
        ajax_pattern = r"<script[^>]*>\s*/\*\s*<!\[CDATA\[\s*\*/\s*var ajax_var\s*=\s*\{[^}]+\};\s*/\*\s*\]\]>\s*\*/\s*</script>"
        html_content = re.sub(ajax_pattern, "", html_content, flags=re.IGNORECASE)
        removals.append("admin-ajax variables")

    # 11. Remove WordPress REST API links
    if "api.w.org" in html_content:
        html_content = re.sub(
            r'\s*<link[^>]*rel="https://api\.w\.org/"[^>]*>\s*', "\n", html_content
        )
        removals.append("REST API links")

    # 12. Remove JSON API links
    if "application/json" in html_content:
        html_content = re.sub(
            r'\s*<link\s+[^>]*type="application/json"[^>]*>\s*', "\n", html_content
        )
        removals.append("JSON API links")

    # 13. Remove EditURI/RSD link
    if "EditURI" in html_content:
        html_content = re.sub(
            r'\s*<link\s+[^>]*rel="EditURI"[^>]*>\s*', "\n", html_content
        )
        removals.append("RSD/EditURI link")

    # 14. Remove WordPress generator meta tag
    if "WordPress" in html_content:
        html_content = re.sub(
            r'\s*<meta[^>]*name="generator"[^>]*content="WordPress[^"]*"[^>]*/?>\s*',
            "\n",
            html_content,
        )
        removals.append("WordPress generator meta")

    # 15. Remove Redux generator meta tag
    if "Redux" in html_content:
        html_content = re.sub(
            r'\s*<meta[^>]*name="generator"[^>]*content="Redux[^"]*"[^>]*/?>\s*',
            "\n",
            html_content,
        )
        removals.append("Redux generator meta")

    # 16. Remove WPBakery generator meta tag
    if "WPBakery" in html_content:
        html_content = re.sub(
            r'\s*<meta[^>]*name="generator"[^>]*content="Powered by WPBakery[^"]*"[^>]*/?>\s*',
            "\n",
            html_content,
        )
        removals.append("WPBakery generator meta")

    # 17. Remove Slider Revolution generator meta tag
    if "Slider Revolution" in html_content:
        html_content = re.sub(
            r'\s*<meta[^>]*name="generator"[^>]*content="Powered by Slider Revolution[^"]*"[^>]*/?>\s*',
            "\n",
            html_content,
        )
        removals.append("Slider Revolution generator meta")

    # 18. Remove shortlink
    if "shortlink" in html_content:
        html_content = re.sub(
            r'\s*<link[^>]*rel="shortlink"[^>]*>\s*', "\n", html_content
        )
        removals.append("shortlink")

    # 19. Remove oEmbed links (both JSON and XML)
    if "oembed" in html_content.lower():
        # Remove oEmbed JSON links
        html_content = re.sub(
            r'\s*<link\s+[^>]*type="application/json\+oembed"[^>]*>\s*',
            "\n",
            html_content,
        )
        # Remove oEmbed XML links (multiline)
        html_content = re.sub(
            r'\s*<link\s+[^>]*type="text/xml\+oembed"[^>]*>\s*', "\n", html_content
        )
        removals.append("oEmbed links")

    # 20. Remove Google Maps callback function (if not using maps)
    if "rgmkInitGoogleMaps" in html_content:
        html_content = re.sub(
            r"<script[^>]*>\s*function rgmkInitGoogleMaps\(\)[\s\S]*?</script>",
            "",
            html_content,
        )
        removals.append("Google Maps callback")

    # 21. Remove Contact Form 7 scripts (requires WordPress backend)
    cf7_scripts = [
        (r'\s*<script[^>]*src="[^"]*contact-form-7[^"]*"[^>]*>\s*</script>\s*', "Contact Form 7 JS"),
        (r'\s*<script[^>]*id="swv-js"[^>]*>\s*</script>\s*', "SWV script"),
        (r'\s*<script[^>]*id="contact-form-7-js[^"]*"[^>]*>[\s\S]*?</script>\s*', "Contact Form 7 inline config"),
    ]
    for pattern, name in cf7_scripts:
        if re.search(pattern, html_content, re.IGNORECASE):
            html_content = re.sub(pattern, "\n", html_content, flags=re.IGNORECASE)
            removals.append(name)

    # 22. Remove WordPress comment reply script (no backend)
    if "comment-reply" in html_content:
        html_content = re.sub(
            r'\s*<script[^>]*id="comment-reply-js"[^>]*>\s*</script>\s*',
            "\n",
            html_content,
            flags=re.IGNORECASE,
        )
        removals.append("Comment reply script")

    # 23. Remove WordPress polyfill (only needed for WP blocks in old browsers)
    if "wp-polyfill" in html_content:
        html_content = re.sub(
            r'\s*<script[^>]*id="wp-polyfill-js"[^>]*>\s*</script>\s*',
            "\n",
            html_content,
            flags=re.IGNORECASE,
        )
        removals.append("WP polyfill")

    # 24. Remove foodfarm-params with admin-ajax URLs (won't work on static)
    if 'foodfarm_params' in html_content or 'admin-ajax.php' in html_content:
        ajax_pattern = r'<script[^>]*id="foodfarm-script-js-extra"[^>]*>\s*/\*\s*<!\[CDATA\[\s*\*/\s*var foodfarm_params\s*=\s*\{[\s\S]*?\};\s*/\*\s*\]\]>\s*\*/\s*</script>'
        if re.search(ajax_pattern, html_content, re.IGNORECASE):
            html_content = re.sub(ajax_pattern, "", html_content, flags=re.IGNORECASE)
            removals.append("Foodfarm ajax params")

    # 25. Remove other admin-ajax variable scripts
    if "admin-ajax.php" in html_content:
        # Generic pattern for any script containing admin-ajax.php
        generic_ajax_pattern = r'<script[^>]*>[^<]*admin-ajax\.php[^<]*</script>'
        if re.search(generic_ajax_pattern, html_content, re.IGNORECASE):
            html_content = re.sub(generic_ajax_pattern, "", html_content, flags=re.IGNORECASE)
            removals.append("admin-ajax variables")

    # 26. Remove wpcf7 form hidden fields (won't work on static site)
    if "_wpcf7" in html_content:
        # Remove the hidden fields div in contact forms
        wpcf7_pattern = r'<div style="display:\s*none">\s*<input[^>]*name="_wpcf7"[^>]*/?>\s*<input[^>]*name="_wpcf7_version"[^>]*/?>\s*<input[^>]*name="_wpcf7_locale"[^>]*/?>\s*<input[^>]*name="_wpcf7_unit_tag"[^>]*/?>\s*<input[^>]*name="_wpcf7_container_post"[^>]*/?>\s*<input[^>]*name="_wpcf7_posted_data_hash"[^>]*/?>\s*</div>'
        if re.search(wpcf7_pattern, html_content, re.IGNORECASE | re.DOTALL):
            html_content = re.sub(wpcf7_pattern, "", html_content, flags=re.IGNORECASE | re.DOTALL)
            removals.append("WPCF7 hidden fields")

    # 27. Remove WordPress form action URLs (replace with # or remove)
    if 'simply_static_page=' in html_content:
        html_content = re.sub(
            r'action="[^"]*\?simply_static_page=\d+#wpcf7-f\d+-p\d+-o\d+"',
            'action="#"',
            html_content
        )
        removals.append("WP form actions")

    # 28. Remove unused time-circles.js (countdown timer - not used on any pages)
    if 'time-circles' in html_content:
        html_content = re.sub(
            r'\s*<script[^>]*src="[^"]*time-circles[^"]*"[^>]*>\s*</script>\s*',
            '\n',
            html_content,
            flags=re.IGNORECASE
        )
        removals.append("time-circles.js (unused)")

    # 29. Remove unused prettyPhoto CSS and JS (lightbox - no triggers found)
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

    # 30. Remove object-cache-pro HTML comments
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
        cleaned_content, removals = remove_wordpress_code(content)
        new_length = len(cleaned_content)

        if original_length != new_length:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(cleaned_content)
            return {
                "file": file_path,
                "bytes_removed": original_length - new_length,
                "removals": removals,
            }
        else:
            return None

    except Exception as e:
        print(f"✗ Error processing {file_path}: {e}")
        return None


def main():
    """Main function to process all HTML files."""
    # Get the script's directory and project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    src_dir = project_root / "src"

    if not src_dir.exists():
        print(f"Error: Directory {src_dir} does not exist")
        print("Make sure this script is in the project root directory")
        return

    html_files = list(src_dir.rglob("*.html"))
    print(f"Found {len(html_files)} HTML files to process\n")
    print("=" * 70)

    modified_files = []
    for i, html_file in enumerate(html_files, 1):
        print(f"\n[{i}/{len(html_files)}] Processing: {html_file.relative_to(src_dir)}")
        result = process_html_file(html_file)
        if result:
            modified_files.append(result)
            print(f"  ✓ Removed {result['bytes_removed']:,} bytes")
            if result["removals"]:
                for removal in result["removals"]:
                    print(f"    - {removal}")
        else:
            print(f"  - No WordPress code found")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Files processed: {len(html_files)}")
    print(f"Files modified: {len(modified_files)}")

    if modified_files:
        total_bytes = sum(f["bytes_removed"] for f in modified_files)
        print(f"Total bytes removed: {total_bytes:,}")
        print("\nModified files:")
        for f in modified_files:
            print(f"  - {f['file'].name}: {f['bytes_removed']:,} bytes")

    print("\nCleanup complete!")


if __name__ == "__main__":
    main()
