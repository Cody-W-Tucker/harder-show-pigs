# AGENTS.md - Coding Guidelines for Harder Show Pigs Website

## Project Overview

Static HTML website converted from WordPress. Uses Python 3 scripts for maintenance and Nix for development environment.

## Development Environment

- **Environment**: Nix flake with direnv (configured in `flake.nix` and `.envrc`)
- **Python**: Version 3 (standard library only - no external dependencies)
- **Source directory**: `src/` contains all HTML files and assets

## Build/Development Commands

```bash
# Start development server on http://localhost:8008
serve

# Stop development server
stop

# View server logs
cat server.log
```

## Python Script Guidelines

### Style Conventions

- **Standard library only** - no external dependencies
- **Type hints** - use for function parameters and return types
- **Pathlib** - use `pathlib.Path` for all file operations
- **UTF-8 encoding** - always specify `encoding='utf-8'` for file I/O
- **Snake case** - for functions, variables, and file names
- **Constants** - UPPER_CASE for module-level constants (e.g., `SRC_DIR`)

### Python Code Patterns

```python
from pathlib import Path
from typing import List, Optional

# Configuration
SRC_DIR = Path("/home/codyt/Projects/harder/src")

# File operations with explicit encoding
def read_file(file_path: Path) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(file_path: Path, content: str) -> None:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
```

### Error Handling

- Use try/except for file operations
- Print user-friendly error messages
- Return early on errors

### CLI Patterns

- Use `argparse` for command-line interfaces
- Default to **dry-run mode** for destructive operations
- Require explicit `--apply` flag to make changes
- Provide helpful epilog with examples

## HTML Files

### File Structure

Six main HTML files in `src/`:
- `index.html` (homepage)
- `about/index.html`
- `our-boars/index.html`
- `our-gallery/index.html`
- `previous-winning/index.html`
- `contact/index.html`

### WordPress Assets

- `src/wp-content/` - themes, plugins, uploads
- `src/wp-includes/` - WordPress core files

## Maintenance Scripts

### Site Updates (`update_site.py`)

```bash
# Dry run (default) - preview changes
python3 update_site.py --copyright 2026

# Apply changes
python3 update_site.py --copyright 2026 --apply

# Search/replace
python3 update_site.py --search "old" --replace "new" --apply

# Find pattern
python3 update_site.py --find "pattern"

# Update contact info
python3 update_site.py --contact phone --value "308-872-5611" --apply
```

### Cleanup Scripts (`cleanup/`)

```bash
# Remove WordPress-specific code
python3 cleanup/cleanup_wordpress.py

# Prepare for GitHub Pages
python3 cleanup/fix_for_github_pages.py

# Shell helper scripts
cleanup/cleanup.sh
cleanup/remove_empty_folders.sh
cleanup/find_unreferenced_wp_files.sh
```

## Safety Guidelines

1. **Always dry-run first** - Run destructive scripts without `--apply` first
2. **Use git** - Review changes with `git diff` before committing
3. **Revert if needed** - Use `git checkout -- <file>` to revert
4. **Test locally** - Use `serve` to test changes locally

## Git Workflow

```bash
# Review changes
git diff

# Stage and commit
git add src/
git commit -m "Description of changes"

# Revert if needed
git checkout -- src/file.html
```

## No Formal Testing

This project has no test suite. Verify changes by:
1. Running scripts in dry-run mode first
2. Reviewing git diffs
3. Testing locally with `serve`
4. Manual verification in browser

## Code Formatting

- No formal linter/formatter configured
- Follow existing code style in each file
- Keep functions focused and well-documented
- Add docstrings for all public functions
