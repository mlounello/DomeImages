#!/usr/bin/env python3
"""
Build script for generating the dome-colors.html gallery page.

Usage:
    python tools/build_dome_color_catalog.py

This script scans the repository root for DOMEHUE_*.webp images (falling back to PNG)
and generates a responsive gallery page with lazy loading for optimal performance.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # repo root
IMAGES_DIR = ROOT  # images are in repo root
OUTPUT_HTML = ROOT / "dome-colors.html"

# Match DOMEHUE images - prefer webp, fallback to png/jpg
PATTERN = re.compile(r"^DOMEHUE_.*\.(webp|png|jpg|jpeg)$", re.IGNORECASE)


def friendly_name(filename: str) -> str:
    """Convert filename to human-readable title.

    Examples:
        DOMEHUE_SienaGreen.webp -> Siena Green
        DOMEHUE_RedWhiteBlue.png -> Red White Blue
    """
    name = filename.rsplit(".", 1)[0]
    name = name.replace("DOMEHUE_", "")
    # Insert space before capital letters (CamelCase -> Camel Case)
    name = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)
    name = name.replace("_", " ")
    return name.strip()


def get_best_image(base_name: str) -> str | None:
    """Get the best available image format (prefer WebP for smaller size)."""
    for ext in ['.webp', '.png', '.jpg', '.jpeg']:
        candidate = IMAGES_DIR / f"{base_name}{ext}"
        if candidate.exists():
            return candidate.name
    return None


def main() -> None:
    # Find all DOMEHUE images and deduplicate by base name (prefer webp)
    seen_bases = {}
    for p in IMAGES_DIR.iterdir():
        if p.is_file() and PATTERN.match(p.name):
            base = p.stem  # filename without extension
            ext = p.suffix.lower()

            # Prefer webp over other formats
            if base not in seen_bases:
                seen_bases[base] = p
            elif ext == '.webp':
                seen_bases[base] = p  # webp wins
            elif seen_bases[base].suffix.lower() != '.webp':
                # Keep first non-webp found
                pass

    files = sorted(seen_bases.values(), key=lambda p: p.name.lower())

    if not files:
        print("No DOMEHUE images found!")
        return

    tiles = []
    for p in files:
        title = friendly_name(p.name)
        tiles.append(f'''
  <div class="tile">
    <div class="imgwrap">
      <img src="{p.name}" alt="{title}" loading="lazy" decoding="async">
    </div>
    <div class="meta">
      <div class="title">{title}</div>
    </div>
  </div>''')

    html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Dome Colors - Siena College</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Oswald&display=swap" rel="stylesheet">
  <style>
    body {{
      margin: 0;
      font-family: Oswald, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
      background: #0b0b0b;
      color: #fff;
    }}
    header {{
      padding: 28px 20px 12px;
      max-width: 1200px;
      margin: 0 auto;
    }}
    h1 {{
      margin: 0 0 6px;
      font-size: 34px;
      letter-spacing: 0.3px;
    }}
    .sub {{
      margin: 0;
      opacity: 0.85;
      font-size: 18px;
    }}
    .grid {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 14px 20px 40px;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 18px;
    }}
    .tile {{
      background: #111;
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 14px;
      overflow: hidden;
      box-shadow: 0 10px 24px rgba(0,0,0,0.35);
    }}
    .imgwrap {{
      width: 100%;
      aspect-ratio: 1 / 1;
      background: #000;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}
    .meta {{
      padding: 12px 14px 14px;
    }}
    .title {{
      font-size: 20px;
      line-height: 1.1;
      margin-bottom: 4px;
    }}
    footer {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 20px 30px;
      opacity: 0.7;
      font-size: 14px;
    }}
  </style>
</head>
<body>
  <header>
    <h1>Dome Colors</h1>
    <p class="sub">Available dome lighting themes for Siena College.</p>
  </header>

  <section class="grid">{''.join(tiles)}
  </section>

  <footer>
    <span style="opacity:0.6;">{len(files)} dome color themes available.</span>
  </footer>
</body>
</html>
'''
    OUTPUT_HTML.write_text(html, encoding="utf-8")
    print(f"✓ Generated {OUTPUT_HTML.name} with {len(files)} color themes.")


if __name__ == "__main__":
    main()
