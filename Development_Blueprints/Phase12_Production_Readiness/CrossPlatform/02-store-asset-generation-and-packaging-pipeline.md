# Phase 12 — App Store & Google Play Asset Generation and Packaging Pipeline

`Development_Blueprints.Phase12_Production_Readiness.CrossPlatform.02-store-asset-generation-and-packaging-pipeline.md`

**Module:** Store Asset Packaging (`tools/asset-pipeline/`, `NoorHeroes/composeApp/`, `.github/workflows/`)  
**Phase:** Phase 12 — Production Readiness & GA Gate (Sequence Item 739)  
**Platform:** CrossPlatform (Android, iOS, Google Play Console, Apple App Store Connect)  
**Depends on:** Phase 1 CI/CD (`CI_CD.06`, `CI_CD.09`), Phase 12 Item 738 (`01-definition-of-done-ga-gate-checklist.md`)  
**Consumed by:** Mobile Release Bundling (`.aab` / `.ipa`), Google Play Console release automation, Apple App Store Connect submission pipeline  
**Sources of truth:** `PRD_Documents/App Icon-Banner/NoorHeroes_App_Icon_Banner_Prompts_and_Specs.md`; `PRD_Documents/App Icon-Banner/all_image_icon_design_prompts.md` §28; `NoorHeroes_Consolidated_Execution_Blueprint.md` §13  
**Status:** ✅ **Blueprint Authored & Verified**  

---

## 1. Objective and Purpose

In mobile applications targeted at children and families, visual assets on the Google Play Store and Apple App Store are the very first trust checkpoint for parents. Store submission rejections due to improper icon dimensions, unexpected alpha channels, non-sRGB color profiles, or truncated adaptive icon safe zones create launch blockers and friction.

This blueprint specifies the **automated store asset generation, verification, and packaging pipeline** (`tools/asset-pipeline/`). It establishes an automated Python CLI and CI/CD gate that ingests high-resolution master SVGs/PNGs and deterministically synthesizes, validates, and packages the complete multi-density asset catalogs for Android (Adaptive Icons, Legacy Mipmaps, Round Icons, Monochrome Themed Icons, Notification Silhouettes, and Android 12+ SplashScreen drawables) and iOS (`AppIcon.appiconset` with full `Contents.json` manifest) along with Google Play Console and Apple App Store Connect marketing collateral.

---

## 2. Scope and Asset Requirements

### 2.1 Brand Identity & Design System Guardrails
All generated assets must strictly conform to the brand tokens specified in `all_image_icon_design_prompts.md` §1 and `CORE_DESIGNSYSTEM_INSTRUCTIONS.md`:
- **Primary Teal:** `#0B5E4A` (Background & Header accents)
- **Deep Warm Teal:** `#0F5E5E` (Adaptive Icon background edge)
- **Mid Warm Teal:** `#1B7A7A` (Adaptive Icon radial center)
- **Accent Gold:** `#C9921A` / `#F0B429` (Crescent moon & star companion motif)
- **Gold Light / Glow:** `#E8B84B` (Gentle outer glow)
- **Pure White Silhouette:** `#FFFFFF` (Push notification status bar icons)
- **Theological & Safety Rules:** Strictly zero realistic human faces or figures; abstract non-human companion ("Noor" lantern/crescent motif); calm and trustworthy aesthetic suitable for ages 3–12.

---

### 2.2 Complete Android Asset Matrix

Android API 26+ enforces adaptive icons separating the **foreground** and **background** layers. Android 13 (API 33+) adds monochrome tinted icons. Pre-Android 8.0 devices require pre-composited legacy square and circular icons.

| Asset Type | Target Path | Canvas Dimensions | Safe Area / Constraints | Format |
|---|---|---|---|---|
| **Adaptive Foreground** | `res/drawable-nodpi/ic_launcher_foreground.png` | 432×432 px (108×108 dp @ xxxhdpi) | Inner 264×264 px (66×66 dp) circular safe zone. Central glowing crescent & star. | 32-bit PNG (Alpha transparency) |
| **Adaptive Background** | `res/drawable-nodpi/ic_launcher_background.png` | 432×432 px (108×108 dp @ xxxhdpi) | Full-bleed radial gradient (`#0F5E5E` to `#1B7A7A`). No transparency. | 24-bit PNG (No alpha) |
| **Adaptive Monochrome** | `res/drawable-nodpi/ic_launcher_monochrome.png` | 432×432 px (108×108 dp @ xxxhdpi) | Inner 264×264 px safe zone. Flat single-color silhouette for Material You theming. | 32-bit PNG (Alpha) |
| **Adaptive Icon XML** | `res/mipmap-anydpi-v26/ic_launcher.xml` | Vector / Layer binding | Pairs foreground and background layers. | Android Vector/XML |
| **Adaptive Round XML** | `res/mipmap-anydpi-v26/ic_launcher_round.xml` | Vector / Layer binding | Pairs foreground and background layers for circular masks. | Android Vector/XML |
| **Legacy mdpi** | `res/mipmap-mdpi/ic_launcher.png` | 48×48 px | Pre-composited foreground on background. | 32-bit PNG |
| **Legacy hdpi** | `res/mipmap-hdpi/ic_launcher.png` | 72×72 px | Pre-composited. | 32-bit PNG |
| **Legacy xhdpi** | `res/mipmap-xhdpi/ic_launcher.png` | 96×96 px | Pre-composited. | 32-bit PNG |
| **Legacy xxhdpi** | `res/mipmap-xxhdpi/ic_launcher.png` | 144×144 px | Pre-composited. | 32-bit PNG |
| **Legacy xxxhdpi** | `res/mipmap-xxxhdpi/ic_launcher.png` | 192×192 px | Pre-composited. | 32-bit PNG |
| **Legacy Round (mdpi–xxxhdpi)** | `res/mipmap-*/ic_launcher_round.png` | 48, 72, 96, 144, 192 px | Circular pre-cropped composite. | 32-bit PNG |
| **Notification Icons** | `res/drawable-*/ic_stat_notify.png` | 24, 36, 48, 72, 96 px | **Pure white silhouette on transparent background.** No color, no glow. | 32-bit PNG |
| **Android 12+ Splash** | `res/drawable-nodpi/ic_splash_brand_icon.png` | 288×288 dp (1152×1152 px) | 240×240 dp (960×960 px) inner safe circle. | 32-bit PNG |

---

### 2.3 Complete iOS Asset Catalog Matrix (`AppIcon.appiconset`)

Apple Xcode requires an `AppIcon.appiconset` asset catalog containing specific point sizes across 1x, 2x, and 3x scale factors, culminating in the 1024×1024 marketing icon.

| Idiom | Usage / Role | Point Size | Scale | Pixel Dimensions | File Name |
|---|---|---|---|---|---|
| **Universal** | App Store Marketing Icon | 1024×1024 pt | 1x | **1024×1024 px** | `icon_1024x1024.png` (Strictly **NO ALPHA**) |
| **iPhone** | Notification | 20×20 pt | 2x | 40×40 px | `icon_20pt@2x.png` |
| **iPhone** | Notification | 20×20 pt | 3x | 60×60 px | `icon_20pt@3x.png` |
| **iPhone** | Settings | 29×29 pt | 2x | 58×58 px | `icon_29pt@2x.png` |
| **iPhone** | Settings | 29×29 pt | 3x | 87×87 px | `icon_29pt@3x.png` |
| **iPhone** | Spotlight | 40×40 pt | 2x | 80×80 px | `icon_40pt@2x.png` |
| **iPhone** | Spotlight | 40×40 pt | 3x | 120×120 px | `icon_40pt@3x.png` |
| **iPhone** | App Launcher | 60×60 pt | 2x | 120×120 px | `icon_60pt@2x.png` |
| **iPhone** | App Launcher | 60×60 pt | 3x | 180×180 px | `icon_60pt@3x.png` |
| **iPad** | Notification | 20×20 pt | 1x | 20×20 px | `icon_20pt@1x.png` |
| **iPad** | Notification | 20×20 pt | 2x | 40×40 px | `icon_20pt@2x.png` |
| **iPad** | Settings | 29×29 pt | 1x | 29×29 px | `icon_29pt@1x.png` |
| **iPad** | Settings | 29×29 pt | 2x | 58×58 px | `icon_29pt@2x.png` |
| **iPad** | Spotlight | 40×40 pt | 1x | 40×40 px | `icon_40pt@1x.png` |
| **iPad** | Spotlight | 40×40 pt | 2x | 80×80 px | `icon_40pt@2x.png` |
| **iPad** | App Launcher | 76×76 pt | 1x | 76×76 px | `icon_76pt@1x.png` |
| **iPad** | App Launcher | 76×76 pt | 2x | 152×152 px | `icon_76pt@2x.png` |
| **iPad Pro** | App Launcher | 83.5×83.5 pt | 2x | 167×167 px | `icon_83.5pt@2x.png` |

---

### 2.4 Store Console Listing & Marketing Assets

| Store | Asset Role | Exact Dimensions | File Constraints |
|---|---|---|---|
| **Google Play** | Hi-res App Icon | **512×512 px** | 32-bit PNG, sRGB color profile, max file size 1,024 KB. |
| **Google Play** | Feature Graphic Banner | **1024×500 px** | JPEG or 24-bit PNG (**strictly no alpha**), max 15MB (target <1.5MB), 16:9 safe center title zone. |
| **Google Play** | Phone Screenshots | 1080×1920 or 1080×2400 px | Min 4 screenshots, 16:9 / 20:9 aspect ratio, JPEG/PNG without alpha. |
| **Google Play** | 7" & 10" Tablet Screenshots | 1200×1920 or 2048×1536 px | Min 2 screenshots per form factor. |
| **App Store** | App Store Product Icon | **1024×1024 px** | PNG without alpha or transparency, 72 dpi, RGB, flattened layers. |
| **App Store** | 6.7" Super Retina Screenshots | 1290×2796 px (portrait) | iPhone 15/16 Pro Max display. |
| **App Store** | 6.5" Display Screenshots | 1242×2688 px (portrait) | iPhone 11 Pro Max / XS Max display. |
| **App Store** | 12.9" iPad Pro Screenshots | 2048×2732 px (portrait) | 6th Generation iPad Pro. |

---

## 3. Technical Architecture & Component Flow

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                            Master Vector Assets                              │
│  • master_icon_foreground.svg (432x432 dp scale, 264dp safe circle)         │
│  • master_icon_background.svg (432x432 dp scale, #0F5E5E radial gradient)   │
│  • master_icon_monochrome.svg (432x432 dp scale, white silhouette)           │
│  • master_feature_banner.svg  (1024x500 px, no-alpha composite)             │
│  • master_notification.svg    (96x96 px, pure flat white silhouette)        │
└──────────────────────────────────────┬───────────────────────────────────────┘
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                    tools/asset-pipeline/generate_store_assets.py              │
│  1. CairoSVG / Pillow Vector Rasterization                                   │
│  2. High-Quality Lanczos Resampling to Target Mipmaps & Densities            │
│  3. Alpha Channel Stripping & sRGB Color Profile Normalization               │
│  4. Safe-Zone Circular Edge Contrast Mask Verification                       │
│  5. Xcode Asset Catalog JSON Synthesis (Contents.json)                       │
└───────────────┬──────────────────────────────┬───────────────────────────────┘
                ▼                              ▼                               ▼
  ┌───────────────────────────┐  ┌───────────────────────────┐   ┌───────────────────────────┐
  │   Android App Resources   │  │    iOS Asset Catalog      │   │    Store Release Bundles  │
  │  res/mipmap-*/ic_launcher │  │  Assets.xcassets/AppIcon  │   │  build/dist/store-assets/ │
  │  res/drawable-*/ic_stat_* │  │  Contents.json + 18 PNGs  │   │  • play_store_icon_512.png│
  │  res/mipmap-anydpi-v26/   │  │  Strict No-Alpha 1024x1024│   │  • feature_banner_1024.jpg│
  └───────────────────────────┘  └───────────────────────────┘   └───────────────────────────┘
                │                              │                               │
                └──────────────────────────────┼───────────────────────────────┘
                                               ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                 CI/CD Automated Gate: test_store_assets.py                   │
│  • Assert zero alpha in 1024x1024 iOS marketing icon & 1024x500 banner       │
│  • Assert exact pixel dimensions across all 35+ generated asset targets      │
│  • Assert file size limits (<1024KB for 512px icon)                          │
│  • Assert pure white pixel values in notification drawables                  │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Directory and File Structure

```text
tools/
└── asset-pipeline/
    ├── master-assets/
    │   ├── master_foreground.svg              # 432x432 vector foreground
    │   ├── master_background.svg              # 432x432 vector background
    │   ├── master_monochrome.svg              # 432x432 vector silhouette
    │   ├── master_notification.svg            # 96x96 flat white silhouette
    │   └── master_feature_banner.svg          # 1024x500 banner graphic
    ├── generate_store_assets.py               # Core Python automation CLI
    ├── requirements.txt                       # Pillow>=10.2.0, cairosvg>=2.7.1
    └── templates/
        └── Contents.json.j2                   # Xcode asset catalog template
NoorHeroes/
├── androidApp/
│   └── src/main/res/
│       ├── mipmap-anydpi-v26/
│       │   ├── ic_launcher.xml                # Adaptive icon XML
│       │   └── ic_launcher_round.xml          # Adaptive round XML
│       ├── mipmap-{mdpi,hdpi,xhdpi,xxhdpi,xxxhdpi}/
│       │   ├── ic_launcher.png                # Composited legacy
│       │   └── ic_launcher_round.png          # Composited round legacy
│       └── drawable-{mdpi,hdpi,xhdpi,xxhdpi,xxxhdpi}/
│           └── ic_stat_notify.png             # Status-bar push icon
└── iosApp/
    └── iosApp/
        └── Assets.xcassets/
            └── AppIcon.appiconset/
                ├── Contents.json              # Apple JSON asset manifest
                └── icon_*.png                 # Generated iOS PNGs
tests/
└── architecture/
    └── test_store_assets.py                   # Automated CI verification suite
```

---

## 5. Automation CLI Script Specification (`generate_store_assets.py`)

The pipeline CLI script must execute idempotently and support both headless CI environments and local designer runs:

```python
#!/usr/bin/env python3
"""
tools/asset-pipeline/generate_store_assets.py
Automated Store Asset Generation & Packaging Pipeline for NoorHeroes
Generates 100% compliant Android and iOS icon sets and store marketing collateral.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from PIL import Image, ImageDraw

ANDROID_MIPMAP_SIZES = {
    "mipmap-mdpi": (48, 48),
    "mipmap-hdpi": (72, 72),
    "mipmap-xhdpi": (96, 96),
    "mipmap-xxhdpi": (144, 144),
    "mipmap-xxxhdpi": (192, 192),
}

ANDROID_NOTIFICATION_SIZES = {
    "drawable-mdpi": (24, 24),
    "drawable-hdpi": (36, 36),
    "drawable-xhdpi": (48, 48),
    "drawable-xxhdpi": (72, 72),
    "drawable-xxxhdpi": (96, 96),
}

IOS_ICON_SPECS = [
    {"idiom": "universal", "size": "1024x1024", "scale": "1x", "pixels": 1024, "filename": "icon_1024x1024.png", "no_alpha": True},
    {"idiom": "iphone", "size": "20x20", "scale": "2x", "pixels": 40, "filename": "icon_20pt@2x.png", "no_alpha": False},
    {"idiom": "iphone", "size": "20x20", "scale": "3x", "pixels": 60, "filename": "icon_20pt@3x.png", "no_alpha": False},
    {"idiom": "iphone", "size": "29x29", "scale": "2x", "pixels": 58, "filename": "icon_29pt@2x.png", "no_alpha": False},
    {"idiom": "iphone", "size": "29x29", "scale": "3x", "pixels": 87, "filename": "icon_29pt@3x.png", "no_alpha": False},
    {"idiom": "iphone", "size": "40x40", "scale": "2x", "pixels": 80, "filename": "icon_40pt@2x.png", "no_alpha": False},
    {"idiom": "iphone", "size": "40x40", "scale": "3x", "pixels": 120, "filename": "icon_40pt@3x.png", "no_alpha": False},
    {"idiom": "iphone", "size": "60x60", "scale": "2x", "pixels": 120, "filename": "icon_60pt@2x.png", "no_alpha": False},
    {"idiom": "iphone", "size": "60x60", "scale": "3x", "pixels": 180, "filename": "icon_60pt@3x.png", "no_alpha": False},
    {"idiom": "ipad", "size": "20x20", "scale": "1x", "pixels": 20, "filename": "icon_20pt@1x.png", "no_alpha": False},
    {"idiom": "ipad", "size": "20x20", "scale": "2x", "pixels": 40, "filename": "icon_20pt@2x.png", "no_alpha": False},
    {"idiom": "ipad", "size": "29x29", "scale": "1x", "pixels": 29, "filename": "icon_29pt@1x.png", "no_alpha": False},
    {"idiom": "ipad", "size": "29x29", "scale": "2x", "pixels": 58, "filename": "icon_29pt@2x.png", "no_alpha": False},
    {"idiom": "ipad", "size": "40x40", "scale": "1x", "pixels": 40, "filename": "icon_40pt@1x.png", "no_alpha": False},
    {"idiom": "ipad", "size": "40x40", "scale": "2x", "pixels": 80, "filename": "icon_40pt@2x.png", "no_alpha": False},
    {"idiom": "ipad", "size": "76x76", "scale": "1x", "pixels": 76, "filename": "icon_76pt@1x.png", "no_alpha": False},
    {"idiom": "ipad", "size": "76x76", "scale": "2x", "pixels": 152, "filename": "icon_76pt@2x.png", "no_alpha": False},
    {"idiom": "ipad", "size": "83.5x83.5", "scale": "2x", "pixels": 167, "filename": "icon_83.5pt@2x.png", "no_alpha": False},
]

def composite_layers(bg_img: Image.Image, fg_img: Image.Image, size: tuple[int, int], round_crop: bool = False) -> Image.Image:
    """Resize and composite foreground over background, with optional circular mask."""
    bg_resized = bg_img.resize(size, Image.Resampling.LANCZOS).convert("RGBA")
    fg_resized = fg_img.resize(size, Image.Resampling.LANCZOS).convert("RGBA")
    
    composited = Image.alpha_composite(bg_resized, fg_resized)
    if round_crop:
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0] - 1, size[1] - 1), fill=255)
        round_output = Image.new("RGBA", size, (0, 0, 0, 0))
        round_output.paste(composited, (0, 0), mask=mask)
        return round_output
    return composited

def strip_alpha_channel(img: Image.Image, bg_color: tuple[int, int, int] = (15, 94, 94)) -> Image.Image:
    """Flatten image to RGB removing any alpha channel to satisfy App Store / Play banner rules."""
    if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
        rgb_img = Image.new("RGB", img.size, bg_color)
        rgb_img.paste(img, mask=img.split()[3] if img.mode == "RGBA" else None)
        return rgb_img
    return img.convert("RGB")
```

---

## 6. Verification and Automated Test Suite (`test_store_assets.py`)

The verification suite runs as a mandatory CI step in GitHub Actions before any release promotion:

```python
"""
tests/architecture/test_store_assets.py
Validates compliance of generated store assets against Apple & Google submission requirements.
"""

import os
import pytest
from PIL import Image

def test_ios_app_store_marketing_icon_zero_alpha():
    """Apple App Store strictly rejects app icons containing transparency or alpha channels."""
    icon_path = "NoorHeroes/iosApp/iosApp/Assets.xcassets/AppIcon.appiconset/icon_1024x1024.png"
    assert os.path.exists(icon_path), f"Missing iOS 1024x1024 icon at {icon_path}"
    
    with Image.open(icon_path) as img:
        assert img.size == (1024, 1024), f"Incorrect dimensions: {img.size}"
        assert img.mode == "RGB", f"App Store icon must be RGB without alpha channel, found: {img.mode}"
        assert "transparency" not in img.info, "Transparency info found in PNG metadata"

def test_play_store_feature_graphic_dimensions_and_alpha():
    """Google Play feature graphic must be exactly 1024x500 with NO alpha."""
    banner_path = "build/dist/store-assets/google-play/feature_graphic_1024x500.png"
    assert os.path.exists(banner_path), f"Missing Play Store feature graphic at {banner_path}"
    
    with Image.open(banner_path) as img:
        assert img.size == (1024, 500), f"Play Store banner must be 1024x500, found {img.size}"
        assert img.mode in ("RGB", "L"), f"Feature graphic must not contain alpha channel, found: {img.mode}"

def test_play_store_app_icon_size_constraint():
    """Google Play app icon must be 512x512 and under 1,024 KB."""
    icon_path = "build/dist/store-assets/google-play/play_store_icon_512x512.png"
    assert os.path.exists(icon_path), f"Missing Play Store 512 icon at {icon_path}"
    
    size_bytes = os.path.getsize(icon_path)
    assert size_bytes <= 1024 * 1024, f"Play Store icon exceeds 1MB: {size_bytes / 1024:.2f} KB"
    with Image.open(icon_path) as img:
        assert img.size == (512, 512), f"Expected 512x512, found {img.size}"

def test_notification_silhouettes_pure_white():
    """Android notification status bar icons must be pure white (#FFFFFF) with alpha masks."""
    notify_path = "NoorHeroes/androidApp/src/main/res/drawable-xxhdpi/ic_stat_notify.png"
    assert os.path.exists(notify_path), f"Missing notification icon at {notify_path}"
    
    with Image.open(notify_path) as img:
        img_rgba = img.convert("RGBA")
        for x in range(img_rgba.width):
            for y in range(img_rgba.height):
                r, g, b, a = img_rgba.getpixel((x, y))
                if a > 0:
                    assert (r, g, b) == (255, 255, 255), f"Non-white pixel ({r},{g},{b}) found at ({x},{y})"

def test_xcode_contents_json_validity():
    """Verify AppIcon.appiconset/Contents.json has all required idioms and image bindings."""
    manifest_path = "NoorHeroes/iosApp/iosApp/Assets.xcassets/AppIcon.appiconset/Contents.json"
    assert os.path.exists(manifest_path)
    
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    assert data.get("info", {}).get("version") == 1
    images = data.get("images", [])
    assert len(images) >= 18, f"Expected at least 18 icon definitions, found {len(images)}"
    for entry in images:
        fn = entry.get("filename")
        assert fn is not None, f"Entry missing filename: {entry}"
        asset_file = os.path.join(os.path.dirname(manifest_path), fn)
        assert os.path.exists(asset_file), f"Bound icon file does not exist on disk: {asset_file}"
```

---

## 7. CI/CD Integration (`.github/workflows/store-assets-pipeline.yml`)

The store asset pipeline is wired into the release process via GitHub Actions:

```yaml
name: Store Assets Generation and Verification Pipeline

on:
  push:
    paths:
      - 'tools/asset-pipeline/**'
      - 'PRD_Documents/App Icon-Banner/**'
  workflow_dispatch:

jobs:
  validate-and-generate-assets:
    name: Build and Verify Mobile Store Asset Catalogs
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Setup Python Runtime
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install System Graphics Dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0

      - name: Install Python Tool Dependencies
        run: |
          pip install Pillow cairosvg pytest

      - name: Execute Store Asset Generation Pipeline
        run: |
          python tools/asset-pipeline/generate_store_assets.py \
            --input-foreground tools/asset-pipeline/master-assets/master_foreground.svg \
            --input-background tools/asset-pipeline/master-assets/master_background.svg \
            --input-monochrome tools/asset-pipeline/master-assets/master_monochrome.svg \
            --input-banner tools/asset-pipeline/master-assets/master_feature_banner.svg \
            --input-notify tools/asset-pipeline/master-assets/master_notification.svg \
            --output-android NoorHeroes/androidApp/src/main/res \
            --output-ios NoorHeroes/iosApp/iosApp/Assets.xcassets/AppIcon.appiconset \
            --output-store build/dist/store-assets

      - name: Run Quality Gate Verification Suite
        run: |
          pytest tests/architecture/test_store_assets.py -v

      - name: Archive Store Ready Assets Package
        uses: actions/upload-artifact@v4
        with:
          name: store-assets-release-bundle
          path: build/dist/store-assets/
          retention-days: 30
```

---

## 8. Store Console Submission Checklist

### 8.1 Google Play Console Release Checklist
- [ ] **App Icon (512×512 px):** Verified 32-bit PNG with alpha, crisp lantern/crescent motif, file size <1MB.
- [ ] **Feature Graphic (1024×500 px):** Verified 24-bit JPEG/PNG with **zero alpha**, safe title text centered.
- [ ] **Target API Level:** Set to API 34+ (Android 14) with full adaptive icon XML and monochrome layer.
- [ ] **Push Notification Silhouette:** Verified pure white drawable on transparent backdrop across all mipmap densities.
- [ ] **Screenshots:** At least 4 phone screenshots (1080×1920) and 2 tablet screenshots (1200×1920) uploaded under Main Store Listing.

### 8.2 Apple App Store Connect Release Checklist
- [ ] **App Store Marketing Icon (1024×1024 px):** Verified RGB without alpha transparency, sRGB color space, unrounded square corners (Apple automatically applies corner masking).
- [ ] **Xcode Asset Catalog (`AppIcon.appiconset`):** `Contents.json` clean with zero warnings, all iPad/iPhone slots filled.
- [ ] **Kids Category Certification:** App Store age rating set to 4+, "Made for Kids" (Ages 6 to 9 primary band) selected, third-party advertising disabled, zero tracking transparency requirements.
- [ ] **Display Screenshots:** 6.7" Super Retina (1290×2796) and 12.9" iPad Pro (2048×2732) uploaded with localized framing.

---

## 9. Definition of Done & Sign-Off Criteria

1. **Deterministic Regeneration:** The CLI script produces bit-identical assets from master SVGs across clean checkouts.
2. **Zero Alpha Compliance:** 100% pass on automated tests rejecting alpha transparency on iOS marketing icons and Play Store feature banners.
3. **Multi-Density Parity:** All 5 Android mipmap densities, adaptive vector XMLs, and 18 iOS asset catalog variants exist on disk and build without warnings.
4. **CI-Enforced Quality Gate:** GitHub Actions workflow verifies dimensions and constraints before any staging/production promotion tag is created.
