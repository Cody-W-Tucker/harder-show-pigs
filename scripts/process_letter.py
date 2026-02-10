#!/usr/bin/env python3
"""
Process yearly letter PDF into optimized web images.

Converts PDF pages to JPEG format with responsive sizes for web display.
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

# Configuration
SRC_DIR = Path("/home/codyt/Projects/harder/src")
UPDATES_DIR = Path("/home/codyt/Projects/harder/updates")

# Image size variants (width x height)
# Based on the current WordPress responsive image setup
SIZES: List[Tuple[int, int, str]] = [
    (232, 300, "232x300"),      # Thumbnail
    (768, 994, "768x994"),      # Tablet
    (791, 1024, "791x1024"),    # Medium
    (1187, 1536, "1187x1536"),  # Large
]

# Full size dimensions (from existing images)
FULL_WIDTH = 1275
FULL_HEIGHT = 1650

# JPEG quality (0-100)
JPEG_QUALITY = 90


def get_pdf_info(pdf_path: Path) -> int:
    """Get the number of pages in a PDF file."""
    try:
        result = subprocess.run(
            ["pdfinfo", str(pdf_path)],
            capture_output=True,
            text=True,
            check=True
        )
        for line in result.stdout.split("\n"):
            if line.startswith("Pages:"):
                return int(line.split(":")[1].strip())
        return 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback: use ImageMagick's identify
        result = subprocess.run(
            ["identify", str(pdf_path)],
            capture_output=True,
            text=True,
            check=True
        )
        return len(result.stdout.strip().split("\n"))


def convert_pdf_page(
    pdf_path: Path,
    page_num: int,
    output_path: Path,
    width: int,
    height: int,
    quality: int = JPEG_QUALITY
) -> None:
    """Convert a single PDF page to optimized JPEG."""
    cmd = [
        "convert",
        "-density", "150",  # DPI for good quality
        f"{pdf_path}[{page_num}]",
        "-resize", f"{width}x{height}",
        "-quality", str(quality),
        "-strip",  # Remove metadata
        "-interlace", "Plane",  # Progressive JPEG
        str(output_path)
    ]
    subprocess.run(cmd, check=True, capture_output=True)


def process_letter(
    pdf_path: Path,
    year: int,
    dry_run: bool = True
) -> List[Path]:
    """
    Process letter PDF into optimized images.
    
    Args:
        pdf_path: Path to the PDF file
        year: Year for the letter (e.g., 2026)
        dry_run: If True, only show what would be done
    
    Returns:
        List of created file paths
    """
    if not pdf_path.exists():
        print(f"Error: PDF not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)
    
    # Get number of pages
    try:
        num_pages = get_pdf_info(pdf_path)
        print(f"PDF has {num_pages} pages")
    except Exception as e:
        print(f"Error reading PDF: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Create output directory
    output_dir = SRC_DIR / "wp-content" / "uploads" / str(year) / "02"
    
    if dry_run:
        print(f"\n[DRY RUN] Would create directory: {output_dir}")
    else:
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"\nCreated directory: {output_dir}")
    
    created_files: List[Path] = []
    
    # Process each page
    for page_idx in range(num_pages):
        page_num = page_idx  # 0-indexed for ImageMagick
        base_name = f"output-{page_idx:03d}"
        
        print(f"\nProcessing page {page_idx + 1}/{num_pages}...")
        
        # Generate full-size image
        full_path = output_dir / f"{base_name}.jpg"
        if dry_run:
            print(f"  [DRY RUN] Would create: {full_path}")
        else:
            convert_pdf_page(
                pdf_path, page_num, full_path,
                FULL_WIDTH, FULL_HEIGHT
            )
            print(f"  Created: {full_path}")
        created_files.append(full_path)
        
        # Generate size variants
        for width, height, size_label in SIZES:
            size_path = output_dir / f"{base_name}-{size_label}.jpg"
            if dry_run:
                print(f"  [DRY RUN] Would create: {size_path}")
            else:
                convert_pdf_page(
                    pdf_path, page_num, size_path,
                    width, height
                )
                print(f"  Created: {size_path}")
            created_files.append(size_path)
    
    return created_files


def main():
    parser = argparse.ArgumentParser(
        description="Process yearly letter PDF into web-optimized images.",
        epilog="""
Examples:
  # Dry run - preview what would be created
  python3 process_letter.py updates/2026/letter.pdf --year 2026
  
  # Actually process the PDF
  python3 process_letter.py updates/2026/letter.pdf --year 2026 --apply
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "pdf_path",
        type=Path,
        help="Path to the PDF file (or directory containing PDF)"
    )
    
    parser.add_argument(
        "--year",
        type=int,
        required=True,
        help="Year for the letter (e.g., 2026)"
    )
    
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually create the images (default is dry-run)"
    )
    
    args = parser.parse_args()
    
    # If path is a directory, look for PDF files
    pdf_path = args.pdf_path
    if pdf_path.is_dir():
        pdf_files = list(pdf_path.glob("*.pdf"))
        if not pdf_files:
            print(f"Error: No PDF files found in {pdf_path}", file=sys.stderr)
            sys.exit(1)
        if len(pdf_files) > 1:
            print(f"Warning: Multiple PDFs found, using first: {pdf_files[0].name}")
        pdf_path = pdf_files[0]
    
    # Process the letter
    try:
        files = process_letter(pdf_path, args.year, dry_run=not args.apply)
        
        if not args.apply:
            print(f"\n{'='*60}")
            print("DRY RUN - No files were actually created")
            print(f"Run with --apply to create {len(files)} images")
            print(f"{'='*60}")
        else:
            print(f"\n{'='*60}")
            print(f"Successfully created {len(files)} images")
            print(f"{'='*60}")
            
    except KeyboardInterrupt:
        print("\n\nInterrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
