# Dome Colors - Siena College

A web-based visualization system for displaying and managing dome lighting color schemes at Siena College.

## Features

- **Real-time Display** (`dome-display.html`): Shows current and upcoming dome colors, designed for embedding in RiseVision/BigTree digital signage
- **Color Gallery** (`dome-colors.html`): Browsable catalog of all available dome lighting themes
- **Optimized Images**: WebP format for fast loading (~60KB vs ~500KB PNG)

## Files

| File | Purpose |
|------|---------|
| `dome-display.html` | Real-time display for digital signage (RiseVision) |
| `dome-colors.html` | Gallery page showing all available colors |
| `DOMEHUE_*.webp` | Optimized dome color images (740x740) |
| `DOMEHUE_*.png` | Original PNG images (kept for compatibility) |
| `sienahall_new.webp` | Optimized background image |
| `tools/build_dome_color_catalog.py` | Build script for regenerating gallery |

## Usage

### Digital Signage (RiseVision)

Embed this URL in your RiseVision HTML widget:
```
https://mlounello.github.io/DomeImages/dome-display.html
```

The display automatically:
- Fetches current/upcoming dome colors from Google Sheets
- Preloads common images for faster display
- Refreshes every 30 seconds
- Shows loading spinners while images load

### Adding New Dome Colors

1. Add your new image as `DOMEHUE_ColorName.png` (740x740 pixels recommended)
2. Convert to WebP for optimal performance:
   ```bash
   cwebp -q 80 DOMEHUE_ColorName.png -o DOMEHUE_ColorName.webp
   ```
3. Regenerate the gallery:
   ```bash
   python3 tools/build_dome_color_catalog.py
   ```
4. Commit and push to GitHub

### Updating the Google Sheet

The display pulls data from a Google Apps Script endpoint. Update your Google Sheet with:
- Event title
- Start date
- End date
- Image URL (pointing to the GitHub-hosted image)

## Performance

Images are optimized for fast loading on digital signage:

| Asset | Original | Optimized | Savings |
|-------|----------|-----------|---------|
| Dome images | ~500 KB (PNG) | ~60 KB (WebP) | 88% |
| Background | 2.0 MB (PNG) | 170 KB (WebP) | 92% |

## Development

Requirements:
- Python 3.8+
- `cwebp` (for image conversion): `brew install webp`

## License

Internal use - Siena College
