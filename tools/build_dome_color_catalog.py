from __future__ import annotations

import os
import re
from pathlib import Path
from typing import List, Tuple
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]  # repo root
IMAGES_DIR = ROOT  # if your PNGs are in repo root; change if in subfolder
OUTPUT_HTML = ROOT / "dome-colors.html"

PATTERN = re.compile(r"^DOMEHUE_.*\.(png|jpg|jpeg|webp)$", re.IGNORECASE)

# If your images are all in a subfolder like DomeImages/, set:
# IMAGES_DIR = ROOT / "DomeImages"

def friendly_name(filename: str) -> str:
    name = filename.rsplit(".", 1)[0]
    name = name.replace("DOMEHUE_", "")
    name = name.replace("_", " ")
    return name.strip()

def main() -> None:
    files = []
    for p in IMAGES_DIR.iterdir():
        if p.is_file() and PATTERN.match(p.name):
            files.append(p)

    files.sort(key=lambda p: p.name.lower())

    tiles = []
    for p in files:
        tiles.append(f"""
  <div class="tile">
    <div class="imgwrap">
      <img src="{p.name}" alt="{friendly_name(p.name)}">
    </div>
    <div class="meta">
      <div class="title">{friendly_name(p.name)}</div>
    </div>
  </div>
""")

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Dome Colors</title>
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
      aspect-ratio: 16 / 9;
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
  <p class="sub">Available dome lighting looks.</p>
</header>

  <section class="grid">
    {''.join(tiles)}
  </section>

  <footer>
  <span style="opacity:0.6;">Current available dome color looks.</span>
</footer>
</body>
</html>
"""
    OUTPUT_HTML.write_text(html, encoding="utf-8")
    print(f"Wrote {OUTPUT_HTML} with {len(files)} tiles.")

if __name__ == "__main__":
    main()