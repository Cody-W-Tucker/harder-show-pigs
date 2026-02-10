# Harder Show Pigs Website

Static HTML website for Harder Show Pigs - a show pig breeding business. This site was converted from WordPress and is now maintained as a static HTML site with Python-based maintenance tools.

## Overview

This is the official website for Harder Show Pigs, showcasing their show pig breeding program, boars, gallery, and contact information.

**Pages:**
- Home (`index.html`)
- About (`about/index.html`)
- Our Boars (`our-boars/index.html`)
- Gallery (`our-gallery/index.html`)
- Previous Winners (`previous-winning/index.html`)
- Contact (`contact/index.html`)

## Development Environment

This project uses [Nix](https://nixos.org/) for reproducible development environments.

### Prerequisites

- [Nix](https://nixos.org/download.html) with flakes enabled
- [direnv](https://direnv.net/) (optional but recommended)

### Setup

```bash
# Enter the development shell
nix develop

# Or with direnv (automatic on cd into directory)
direnv allow
```

### Available Commands

| Command | Description |
|---------|-------------|
| `serve` | Start development server on http://localhost:8008 |
| `stop` | Stop the development server |
| `cat server.log` | View server logs |

## Project Structure

```
.
├── src/                          # Website source files
│   ├── index.html               # Homepage
│   ├── about/                   # About page
│   ├── our-boars/               # Boars page
│   ├── our-gallery/             # Gallery page
│   ├── previous-winning/        # Previous winners page
│   ├── contact/                 # Contact page
│   ├── wp-content/              # WordPress themes, plugins, uploads
│   └── wp-includes/             # WordPress core files
├── scripts/                     # Utility scripts
│   ├── update_year.py           # Update copyright year
│   └── process_letter.py        # Process show pig letters
├── cleanup/                     # Cleanup and migration scripts
│   ├── cleanup_wordpress.py     # Remove WordPress-specific code
│   ├── fix_for_github_pages.py  # Prepare for GitHub Pages
│   └── *.sh                     # Shell helper scripts
├── update_site.py               # Main site update script
├── flake.nix                    # Nix flake configuration
└── AGENTS.md                    # Detailed coding guidelines
```

## Maintenance

### Site Updates

The `update_site.py` script provides various site maintenance operations:

```bash
# Update copyright year (dry run - preview changes)
python3 update_site.py --copyright 2026

# Update copyright year (apply changes)
python3 update_site.py --copyright 2026 --apply

# Search and replace text
python3 update_site.py --search "old text" --replace "new text" --apply

# Find patterns in files
python3 update_site.py --find "pattern"

# Update contact information
python3 update_site.py --contact phone --value "308-872-5611" --apply
```

**Important:** Always run commands without `--apply` first to preview changes!

### Cleanup Scripts

Scripts in the `cleanup/` directory help prepare the site for different hosting platforms:

```bash
# Remove WordPress-specific code
python3 cleanup/cleanup_wordpress.py

# Prepare for GitHub Pages
python3 cleanup/fix_for_github_pages.py
```

## Deployment

### GitHub Pages

To deploy the site to GitHub Pages:

```bash
# Push the src/ directory to the gh-pages branch
git subtree push --prefix src origin gh-pages
```

This command pushes only the `src/` folder to the `gh-pages` branch, which GitHub Pages serves from. The site will be available at `https://hardershowpigs.github.io/harder/`.

**Requirements:**
- Push access to the repository
- GitHub Pages enabled in repository settings (source: gh-pages branch)

## Technology Stack

- **HTML5** - Static site markup
- **CSS3** - Styling (originally WordPress FoodFarm theme)
- **Python 3** - Maintenance scripts (standard library only)
- **Nix** - Development environment and dependencies

## WordPress Assets

The site retains WordPress assets in `src/wp-content/` and `src/wp-includes/` for:
- Theme stylesheets and scripts
- Uploaded images and media
- Plugin assets (Redux Framework, FoodFarm shortcodes)

These are served as static files and do not require a WordPress backend.

## Guidelines

See [AGENTS.md](./AGENTS.md) for detailed coding guidelines and project conventions.

Key points:
- Always dry-run destructive scripts first
- Use `git` to track changes
- Test locally with `serve` before deploying
- Python scripts use only standard library
- Use `pathlib.Path` for file operations
- Specify UTF-8 encoding for all file I/O

## License

Copyright © 2026 HarderShowPigs. All rights reserved.

## Contact

For questions about this codebase, contact the site administrator.
