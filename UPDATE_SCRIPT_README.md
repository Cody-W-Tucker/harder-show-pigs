# Site Update Script

A Python script to manage updates across all HTML files in the `src/` directory.

## Usage

The script runs in **dry-run mode by default** - it will show you what would change without actually modifying files. Use `--apply` to make changes.

### Common Commands

```bash
# Update copyright year (dry run first)
python3 update_site.py --copyright 2026

# Actually apply the copyright update
python3 update_site.py --copyright 2026 --apply

# Search and replace text
python3 update_site.py --search "old text" --replace "new text"

# Apply the search/replace
python3 update_site.py --search "old text" --replace "new text" --apply

# Find text across all files (regex supported)
python3 update_site.py --find "facebook\.com"

# Update Facebook URL
python3 update_site.py --facebook "https://facebook.com/new-page-url" --apply

# Update contact information
python3 update_site.py --contact phone --value "308-872-5611" --apply
python3 update_site.py --contact email --value "newemail@example.com" --apply
python3 update_site.py --contact address --value "123 New Address" --apply
```

## Features

- **Dry-run by default**: Preview changes before applying them
- **Updates all 6 HTML files**:
  - `src/index.html`
  - `src/about/index.html`
  - `src/our-boars/index.html`
  - `src/previous-winning/index.html`
  - `src/our-gallery/index.html`
  - `src/contact/index.html`

## Safety

1. Always run without `--apply` first to preview changes
2. Use `git diff` to review changes before committing
3. Use `git checkout -- <file>` to revert if needed

## Examples

### Update Footer Copyright
```bash
python3 update_site.py --copyright 2026 --apply
```

### Change Phone Number
```bash
python3 update_site.py --contact phone --value "308-555-1234" --apply
```

### Search for Text
```bash
python3 update_site.py --find "Harder Show Pigs"
```

### Custom Search/Replace
```bash
# Replace old email with new one
python3 update_site.py --search "old@email.com" --replace "new@email.com" --apply
```
